from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
from django.core.files.storage import default_storage

from . import util

import markdown2
import random

class SearchForm(forms.Form):
    q = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia", "class": "search"}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", required=True, min_length=3, max_length=25, widget=forms.TextInput(attrs={"placeholder": "Enter title", "class": "form-control"}))
    body = forms.CharField(label="Body", required=True, min_length=10, max_length=500, widget=forms.Textarea(attrs={"placeholder": "Enter body", "class": "form-control"}))

class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", required=True, min_length=3, max_length=25, widget=forms.TextInput(attrs={"class": "form-control"}))
    body = forms.CharField(label="Body", required=True, min_length=10, max_length=500, widget=forms.Textarea(attrs={"class": "form-control"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })

def entry(request, title):
    # Get markdown file
    md_page = util.get_entry(title)

    # If page exists
    if md_page:
        # Convert markdown file to HTML
        html_page = markdown2.markdown(md_page)
        
        # Render template
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html_page": html_page,
            "search_form": SearchForm()
        })
    # If page doesn't exist
    else:
        # Render 404 template
        return render(request, "encyclopedia/404.html", {"search_form": SearchForm() }, status=404)

def random_page(request):
    # Get a random entry
    random_entry_title = random.choice(util.list_entries())

    # Get markdown file
    md_page = util.get_entry(random_entry_title)

    # Convert markdown file to HTML
    html_page = markdown2.markdown(md_page)
        
    # Render template
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry_title,
        "html_page": html_page,
        "search_form": SearchForm()
    })

def search(request):
    query = request.POST.get("q")
    if query in util.list_entries():
        return redirect("wiki:entry", title=query)
    else:
        search_list = []
        for entry in util.list_entries():
            if query in entry:
                search_list.append(entry)   
        return render(request, "encyclopedia/search_results.html", {
            "search_list": search_list,
            "search_form": SearchForm()
        })

def new_page(request):
    if request.method == "POST":
        new_page_form = NewPageForm(request.POST)
        if new_page_form.is_valid():
            new_page_title = new_page_form.cleaned_data["title"]
            new_page_body = new_page_form.cleaned_data["body"]
            all_entries = util.list_entries()
            for entry_title in all_entries:
                if entry_title.lower() == new_page_title.lower():
                    return render(request, "encyclopedia/new_page.html", {
                        "search_form": SearchForm(),
                        "new_page_form": new_page_form,
                        "error": "This page already exists"
                    })
            new_page_title_md = "# " + new_page_title
            new_page_body_md = "\n" + new_page_body
            new_page_content_md = new_page_title_md + new_page_body_md
            util.save_entry(new_page_title, new_page_content_md)
            html_page = markdown2.markdown(util.get_entry(new_page_title))
            return render(request, "encyclopedia/entry.html", {
                "title": new_page_title,
                "html_page": html_page,
                "search_form": SearchForm()
            })                    

    return render(request, "encyclopedia/new_page.html", {
        "new_page_form": NewPageForm(),
        "search_form": SearchForm()
    })

def edit_page(request, title):
    entry_page = util.get_entry(title)
    edit_page_form = EditPageForm(initial={"title": title, "body": entry_page})
    return render(request, "encyclopedia/edit_page.html", {
        "search_form": SearchForm(),
        "edit_page_form": edit_page_form,
        "title": title,
        "body": entry_page
    })

def submit_edits(request, title):
    edit_page_form = EditPageForm()
    if request.method == "POST":
        edit_page_form = EditPageForm(request.POST)
        if edit_page_form.is_valid():
            edit_page_form_title = edit_page_form.cleaned_data["title"]
            edit_page_form_body = edit_page_form.cleaned_data["body"]
            old_page_body_md = util.get_entry(title)
            if edit_page_form_body != old_page_body_md:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
                    edit_page_form_body
                    util.save_entry(edit_page_form_title, edit_page_form_body)
            return redirect("wiki:entry", title=edit_page_form_title)
    return render(request, "encyclopedia/edit_page.html", {
        "search_form": SearchForm(),
        "edit_page_form": edit_page_form
    })