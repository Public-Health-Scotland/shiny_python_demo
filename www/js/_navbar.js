function closeDropdownMenu() {
  console.log('Try to hide dropdown...');

  const dropdownToggle = document.querySelector('.dropdown-toggle');
  if (dropdownToggle) {
    dropdownToggle.classList.remove('show');
    dropdownToggle.setAttribute('aria-expanded', 'false');
    
    // Find the dropdown menu within the parent container
    const parent = dropdownToggle.closest('.nav-item');
    if (parent) {
      const dropdownMenu = parent.querySelector('.dropdown-menu');
      if (dropdownMenu) {
        dropdownMenu.classList.remove('show');
        console.log('Dropdown menu hidden');
      }
    }
  }
  
  // Close the navbar toggler (hamburger menu)
  const navbarToggler = document.querySelector('.navbar-toggler');
  if (navbarToggler) {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
      navbarToggler.classList.remove('collapse', 'show');
      navbarCollapse.classList.remove('show');
      navbarToggler.setAttribute('aria-expanded', 'false');
      console.log('Navbar toggler closed');
    }
  }
}

document.addEventListener('click', function(event) {
  console.log('Triggered click...');
  const navItem = event.target.closest('.nav-item');
  if (navItem && !navItem.classList.contains('dropdown')) {
    closeDropdownMenu();
  }
});

// Change navbar height variable based on scroll position
// window.addEventListener("scroll", function () {
//   const root = document.documentElement;

//   if (window.scrollY > 50) {
//     // Switch to scrolled height
//     root.style.setProperty("--navbar-height", "var(--navbar-height-scrolled)");
//   } else {
//     // Switch back to normal height
//     root.style.setProperty("--navbar-height", "var(--navbar-height-default)");
//   }
// });
