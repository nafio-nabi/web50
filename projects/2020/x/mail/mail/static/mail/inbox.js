document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (mailbox === 'sent') {
    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {
      for (let i = 0; i < emails.length; i++) {
        let element = document.createElement('div');
        element.style.border = '2px solid black';
        element.style.padding = '5px';
        if (emails[id=i].read === true) {
          element.style.backgroundColor = 'gray';
        } else {
          element.style.backgroundColor = 'white';
        }
        element.innerHTML = `<a href="#">${emails[id=i].sender} ${emails[id=i].subject} ${emails[id=i].timestamp}</a>`;
        document.querySelector('#emails-view').append(element);
        element.addEventListener('click', function() {
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#email-detail-view').style.display = 'block';
          document.querySelector('#email-detail-view').innerHTML = '';
          let emailView = document.createElement('div');
          emailView.innerHTML = `<b>From</b>: ${emails[id=i].sender}<br> <b>To</b>: ${emails[id=i].recipients} <br> <b>Subject</b>: ${emails[id=i].subject} <br> <b>Timestamp</b>: ${emails[id=i].timestamp} <hr> ${emails[id=i].body}`;
          document.querySelector('#email-detail-view').append(emailView);
          fetch(`/emails/${emails[id=i].id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
        });
      }
    });
  } else if (mailbox === 'inbox') {
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
      for (let i = 0; i < emails.length; i++) {
        let element = document.createElement('div');
        element.style.border = '2px solid black';
        element.style.padding = '5px';
        if (emails[id=i].read === true) {
          element.style.backgroundColor = 'gray';
        } else {
          element.style.backgroundColor = 'white';
        }
        element.innerHTML = `<a href="#">${emails[id=i].sender} ${emails[id=i].subject} ${emails[id=i].timestamp}</a>`;
        document.querySelector('#emails-view').append(element);
        element.addEventListener('click', function() {
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#email-detail-view').style.display = 'block';
          document.querySelector('#email-detail-view').innerHTML = '';
          let emailView = document.createElement('div');
          emailView.innerHTML = `<b>From</b>: ${emails[id=i].sender}<br> <b>To</b>: ${emails[id=i].recipients} <br> <b>Subject</b>: ${emails[id=i].subject} <br> <b>Timestamp</b>: ${emails[id=i].timestamp} <br> <a href="#" class='btn btn-primary mt-2 mr-2' id='archive-btn'>Archive</a> <a href="#" class='btn btn-primary mt-2' id='reply-btn'>Reply</a> <hr> ${emails[id=i].body}`;
          document.querySelector('#email-detail-view').append(emailView);
          fetch(`/emails/${emails[id=i].id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          let archiveBtn = document.querySelector('#archive-btn');
          archiveBtn.addEventListener('click', function() {
            fetch(`/emails/${emails[id=i].id}`, {
              method: 'PUT',
              body: JSON.stringify({
                archived: true
              })
            })
            .then(response => load_mailbox('inbox'));
          });
          let replyBtn = document.querySelector('#reply-btn');
          replyBtn.addEventListener('click', function() {
            compose_email();

            document.querySelector('#compose-recipients').value = emails[id=i].sender;
            subjectLine = emails[id=i].subject;
            reString = 'Re: ';
            if (subjectLine.includes(reString)) {
              document.querySelector('#compose-subject').value = subjectLine;
            } else {
              document.querySelector('#compose-subject').value = "Re: " + subjectLine;
            }

            let composeBody = document.querySelector('#compose-body');
            composeBody.value = `On ${emails[id=i].timestamp} ${emails[id=i].sender} wrote:` + ' ' + emails[id=i].body;
          });
        });
      }
    });
  } else if (mailbox === 'archive') {
    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
      for (let i = 0; i < emails.length; i++) {
        let element = document.createElement('div');
        element.style.border = '2px solid black';
        element.style.padding = '5px';
        if (emails[id=i].read === true) {
          element.style.backgroundColor = 'gray';
        } else {
          element.style.backgroundColor = 'white';
        }
        element.innerHTML = `<a href="#">${emails[id=i].sender} ${emails[id=i].subject} ${emails[id=i].timestamp}</a>`;
        document.querySelector('#emails-view').append(element);
        element.addEventListener('click', function() {
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#email-detail-view').style.display = 'block';
          document.querySelector('#email-detail-view').innerHTML = '';
          let emailView = document.createElement('div');
          emailView.innerHTML = `<b>From</b>: ${emails[id=i].sender}<br> <b>To</b>: ${emails[id=i].recipients} <br> <b>Subject</b>: ${emails[id=i].subject} <br> <b>Timestamp</b>: ${emails[id=i].timestamp} <br> <a href="#" class='btn btn-primary mt-2' id='unarchive-btn'>Unarchive</a> <hr> ${emails[id=i].body}`;
          document.querySelector('#email-detail-view').append(emailView);
          fetch(`/emails/${emails[id=i].id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          let unarchiveBtn = document.querySelector('#unarchive-btn');
          unarchiveBtn.addEventListener('click', function() {
            fetch(`/emails/${emails[id=i].id}`, {
              method: 'PUT',
              body: JSON.stringify({
                archived: false
              })
            })
            .then(response => load_mailbox('inbox'));
          });
        });
      }
    });
  }
}

function send_mail(event) {
  event.preventDefault()

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => load_mailbox('sent'));
}