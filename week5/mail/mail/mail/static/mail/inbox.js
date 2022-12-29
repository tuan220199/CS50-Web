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

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //get a request to email/mailbox to request email with FETCH 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    //console.log(emails);

    // Extract the items of email objects in an array of emails
    emails.forEach(function(email){       
       
      // Extract each key-value pair from email object, storage in variable
      const email_id = email["id"];
      const sender = email["sender"];
      const recipients = email["recipients"];
      const subject = email["subject"];
      const body = email["body"];
      const timestamp = email["timestamp"];
      const read = email["read"];
      const archived = email["archived"]; 

      // Create the new div element for each email element
      const element = document.createElement('div');
      element.className = "card";
      // Check if the meail read or not 
      if (read === true)
      {
        element.classList.add('bg-secondary'); 
      }
      else
      {
        element.classList.add('bg-white');
      }
      
      // Create card body element 
      const card_body_element = document.createElement('div');
      card_body_element.className = "card-body";

      // Create card text element
      const card_text_element = document.createElement('div');
      card_text_element.className = "card-text";
      card_text_element.innerHTML= `
      <table class="table table-borderless">
        <tbody>
        <tr>
          <td style="width:15%; text-align: left"><strong>${sender}</strong></td>
          <td style="width:15%; text-align: left">${subject}</td>
          <td style="width:70%; text-align: right"><small class="text-muted">${timestamp}</small></td>
        </tr>
        </tbody>
      </table>
      `;
      
      // Append child (HTML element) into card body element
      card_body_element.appendChild(card_text_element);

      // Check the which kind of mailbox: Inbox (add archive button); Archive (add unarchive button); Sent (nothing)
      if (mailbox === "inbox")
      {
        // Archive button created and append as child in card body element
        const archive_button_element = document.createElement("button");
        archive_button_element.className = "btn btn-danger";
        archive_button_element.innerHTML = "Archive";
        card_body_element.appendChild(archive_button_element);
        
        // Click button event on archive: move to archive route and perform animation hide
        archive_button_element.addEventListener('click', function(){
          fetch(`emails/${email_id}`, {
            method: "PUT",
            body: JSON.stringify({
              archived: true
            })
          })
          element.style.animationPlayState = 'running';
          element.addEventListener('animationend', () =>  {
            element.remove();
            });
        }); 
        
      }
      else if (mailbox === "archive")
      {
        // Unarchived button created and append as child in card body element 
        const unarchive_button_element = document.createElement("button");
        unarchive_button_element.className = "btn btn-danger";
        unarchive_button_element.innerHTML = "Unarchive";
        card_body_element.appendChild(unarchive_button_element);
        
        // Click button event on archive: move to archive route and perform animation hide
        unarchive_button_element.addEventListener('click', function(){
          fetch(`emails/${email_id}`, {
            method: "PUT",
            body: JSON.stringify({
              archived: false
            })
          })
          .then(() =>{
            load_mailbox("inbox");
          })
        });
      }
      // Append child (HTML element= card body element) into card element
      element.appendChild(card_body_element);
      
      // Click email and go to view_email function
      card_text_element.addEventListener('click', () => view_email(email_id)); 

     // Append the whole element for each email in the email view 
      document.querySelector('#emails-view').append(element);
    });   
  });

  // when scroll the page, in the end of page set alert and change the background color
  window.onscroll = () => {

    if ((window.innerHeight + window.scrollY >= document.body.offsetHeight) && (localStorage.getItem('alerted') === "false")) 
    {   
          document.querySelector('body').style.background = 'green';
          alert("You have reached all the emails!");
          localStorage.setItem('alerted', "true");  
    } 
    else 
    {
        document.querySelector('body').style.background = 'white';
        localStorage.setItem('alerted', "false");
    }

};

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

function view_email(email_id)
{

  // Check all the email in this user in term of email ID matching email_id

  // Mark the email is already read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // Show the email in detail
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Extract the varible from email
      const sender = email["sender"];
      const recipients = email["recipients"];
      const subject = email["subject"];
      const timestamp = email["timestamp"];
      const body = email["body"];
       
      // Show the mailbox and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#email-detail').style.display = 'block';

      // Show the mailbox in detail
      
      // heaidng email
      const heading_element = document.createElement("div");
      
      heading_element.innerHTML = `
      <br>
      <p><strong>From:</strong> ${sender}</p>
      <p><strong>To:</strong> ${recipients}</p>
      <p><strong>Subject:</strong> ${subject}</p>
      <p><strong>Timestamp:</strong> ${timestamp}</p>
      `;
      heading_element.className = "card";
      // Clear the previous detail email
      document.querySelector('#email-detail').innerHTML = "";

      // Add the element to the email detail
      document.querySelector('#email-detail').append(heading_element);

      // body email
      const body_element = document.createElement("div");
      body_element.innerHTML = `
      <br>
      ${body}
      <br>
      `;
      body_element.className = "card";

      // Add the element to the email view
      document.querySelector('#email-detail').append(body_element);

      // Reply button 
      const button_element = document.createElement("button");
      button_element.className = "btn btn-primary";
      button_element.innerHTML = "Reply";

      // Click button event on reply
      button_element.addEventListener('click', function(){
        email_reply(email_id);
      }); 

      document.querySelector('#email-detail').append(button_element);

      // Archive button 
      const archive_button_element = document.createElement("button");
      archive_button_element.className = "btn btn-danger";
      archive_button_element.innerHTML = "Archive";

      // Click button event on archive
      archive_button_element.addEventListener('click', function(){
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: true
          })
        })
        .then(() => {load_mailbox("archive")})
      }); 

      document.querySelector('#email-detail').append(archive_button_element);
  });
}

function email_reply(email_id)
{
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail').style.display = 'none';

  // Show the email in detail
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Extract the varible from email
      const sender = email["sender"];
      const recipients = email["recipients"];
      const subject = email["subject"];
      const timestamp = email["timestamp"];
      const body = email["body"];


      // Clear out composition fields
      document.querySelector('#compose-recipients').value = sender;
      document.querySelector('#compose-subject').value = `Re: ${body}`;
      document.querySelector('#compose-body').value = `${timestamp} ${sender} wrote: ${body}`;
  })
}