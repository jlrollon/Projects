function modal() {
      const modal = document.querySelector('.open-modal');
      modal.style.display = "block";
}

function updateRow() {
      const modal = document.querySelector('.open-update-modal');
      modal.style.display = "block";
}

function closeModal() {
      const modal = document.querySelector('.open-modal');
      const modalupdate = document.querySelector('.open-update-modal');
      modal.style.display = "none";
      modalupdate.style.display = "none";
}

setTimeout(function() {
      const msg = document.querySelector('.msg-box');
      msg.style.display = "none";
}, 2000);