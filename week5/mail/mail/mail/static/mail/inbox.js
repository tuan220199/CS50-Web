document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //Send email 
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //get a request to email/mailbox to request email with FETCH 
  fetch('/emails/inbox')
  .then(response => response.json())
  .then(emails => {
    // Print emails
    //console.log(emails);

    // Extract the items of email objects in an array of emails
    emails.forEach(function(email){       
       
      // Extract each key-value pair in email object
      const sender = email["sender"];
      const recipients = email["recipients"];
      const subject = email["subject"];
      const body = email["body"];
      const timestamp = email["timestamp"];
      const read = email["read"];
      const archived = email["archived"]; 

      // Create the new div element
      const element = document.createElement('div');
      element.innerHTML = `${sender}   ${body}`;
      document.querySelector('#emails-view').append(element);
    }); 
  });
}

function send_email(event)
{
  // Prevent the event to be submitted and show the result in console
  event.preventDefault();
  //console.log("HI");
  // Retrieve data from HTML file to Java Script file
  recipient = document.querySelector('#compose-recipients');
  subject = document.querySelector('#compose-subject');
  body = document.querySelector('#compose-body');

  // Disable submit button by default:
  //submit.disabled = true;

  // Check the email susscessful or not 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipient.value,
        subject: subject.value,
        body: body.value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });

}