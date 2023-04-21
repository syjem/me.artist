const header = document.getElementById('header');

window.addEventListener('scroll', function() {
  if (window.pageYOffset > 0) {
    header.style.backgroundColor = '#282834'; // Change background color as you desire
  } else {
    header.style.backgroundColor = 'transparent';
  }
});