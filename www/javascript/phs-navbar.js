/**
 * PHS Navbar Enhancement
 *
 * Provides mobile navbar UX improvements:
 * - Adds backdrop overlay when navbar is open
 * - Click outside to close
 * - Click nav link to close
 * - Escape key to close
 * - ARIA attributes for accessibility
 */
(function() {
  'use strict';

  function updateNavbarOnScroll() {
    const nav = document.querySelector('.navbar');
    if (!nav) return;
    const body = document.body;
    const banner = document.querySelector('.phs-banner');
    const tab_content = document.querySelector('.tab-content');

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) {
          nav.classList.add('shrunk');
          body.classList.add('shrunk');
          banner.classList.add('shrunk');
          tab_content.classList.add('shrunk');
        } else {
          nav.classList.remove('shrunk');
          body.classList.remove('shrunk');
          banner.classList.remove('shrunk');
          tab_content.classList.remove('shrunk');
        }
      },
      { threshold: [1.0] }
    );

    const sentinel = document.createElement('div');
    sentinel.style.position = 'absolute';
    sentinel.style.top = '0';
    sentinel.style.width = '100%';
    sentinel.style.height = '1px';
    
    document.body.appendChild(sentinel);

    observer.observe(sentinel);
  }

  function closeNavbar() {
    var collapse = document.querySelector('.navbar-collapse');
    if (!collapse || !collapse.classList.contains('show')) return;

    // Check if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
      var bsCollapse = bootstrap.Collapse.getInstance(collapse);
      if (bsCollapse) bsCollapse.hide();
    }
  }

  function isMobileView() {
    return window.innerWidth < 992; // Bootstrap's lg breakpoint
  }

  /**
   * Prevent dropdowns from auto-opening when navigating to pages inside them.
   * bslib adds .show class directly (doesn't fire Bootstrap events), so we need
   * to watch the DOM for class changes using MutationObserver.
   */
  function preventAutoOpenDropdowns(navbar) {
    var userClickedToggle = null;
    var clickTimestamp = 0;

    // Track user-initiated dropdown opens (mouse, keyboard, touch)
    function markUserInteraction(toggle) {
      if (toggle && toggle.closest('.navbar')) {
        userClickedToggle = toggle;
        clickTimestamp = Date.now();
      }
    }

    // Track mouse clicks
    document.addEventListener('mousedown', function(e) {
      var toggle = e.target.closest('.dropdown-toggle');
      if (toggle) markUserInteraction(toggle);
    }, true);

    // Track keyboard navigation (Enter and Space keys)
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        var toggle = e.target.closest('.dropdown-toggle');
        if (toggle) markUserInteraction(toggle);
      }
    }, true);

    // Track touch events for mobile
    document.addEventListener('touchstart', function(e) {
      var toggle = e.target.closest('.dropdown-toggle');
      if (toggle) markUserInteraction(toggle);
    }, true);

    // Watch for .show class being added to dropdown menus using MutationObserver
    var observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          var element = mutation.target;

          // Check if this is a dropdown menu that just got .show class
          if (element.classList.contains('dropdown-menu') &&
              element.classList.contains('show') &&
              element.closest('.navbar')) {

            // Find the toggle for this dropdown
            var dropdown = element.closest('.dropdown');
            var toggle = dropdown ? dropdown.querySelector('.dropdown-toggle') : null;

            // Check if user interacted with this specific toggle recently (within 500ms)
            // Increased from 200ms to give more time for click events to propagate
            var isRecentUserClick = toggle === userClickedToggle &&
                                   (Date.now() - clickTimestamp) < 500;

            // Also check if dropdown is in desktop mode (not collapsed mobile navbar)
            // In desktop mode, dropdowns should be allowed to open
            var isDesktopMode = !isMobileView();

            if (!isRecentUserClick && !isDesktopMode) {
              // Auto-opened dropdown in mobile collapsed navbar - close it immediately
              element.classList.remove('show');
              if (dropdown) {
                dropdown.classList.remove('show');
              }

              // Also close via Bootstrap API if instance exists
              if (toggle && typeof bootstrap !== 'undefined' && bootstrap.Dropdown) {
                var bsDropdown = bootstrap.Dropdown.getInstance(toggle);
                if (bsDropdown) {
                  bsDropdown.hide();
                }
              }
            } else {
              // User-initiated dropdown OR desktop mode - allow it to stay open
              setTimeout(function() {
                userClickedToggle = null;
              }, 250);
            }
          }
        } else if (mutation.type === 'childList') {
          // New nodes added - check if any are dropdown menus and observe them
          mutation.addedNodes.forEach(function(node) {
            if (node.nodeType === 1) { // Element node
              // Check if the node itself is a dropdown menu
              if (node.classList && node.classList.contains('dropdown-menu')) {
                observer.observe(node, {
                  attributes: true,
                  attributeFilter: ['class']
                });
              }
              // Check if the node contains dropdown menus
              if (node.querySelectorAll) {
                var newMenus = node.querySelectorAll('.dropdown-menu');
                newMenus.forEach(function(menu) {
                  observer.observe(menu, {
                    attributes: true,
                    attributeFilter: ['class']
                  });
                });
              }
            }
          });
        }
      });
    });

    // Observe all existing dropdown menus
    var dropdownMenus = navbar.querySelectorAll('.dropdown-menu');
    dropdownMenus.forEach(function(menu) {
      observer.observe(menu, {
        attributes: true,
        attributeFilter: ['class']
      });
    });

    // Also observe the navbar for new dropdowns being added (handles dynamic content)
    observer.observe(navbar, {
      childList: true,
      subtree: true
    });
  }

  function updateCollapsePosition() {
    var navbar = document.querySelector('.navbar');
    var collapse = document.querySelector('.navbar-collapse');

    if (!navbar || !collapse) return;

    // Get navbar height (always from top of viewport, not current scroll position)
    var navbarRect = navbar.getBoundingClientRect();
    var navbarHeight = navbarRect.height;
    var navbarTop = navbarRect.top + window.pageYOffset; // Account for scroll

    // For fixed positioning, use the height directly (not scroll-adjusted position)
    collapse.style.top = navbarHeight + 'px';

    // Calculate max height for collapse (viewport - navbar - small buffer)
    var maxHeight = window.innerHeight - navbarHeight - 20; // 20px buffer
    collapse.style.maxHeight = maxHeight + 'px';

    // Set CSS custom property for backdrop positioning
    navbar.style.setProperty('--phs-navbar-height', navbarHeight + 'px');
  }


  function init() {
    var navbar = document.querySelector('.navbar');
    var collapse = document.querySelector('.navbar-collapse');

    if (!navbar || !collapse) return;

    // Wait for Bootstrap to be loaded before initializing
    if (typeof bootstrap === 'undefined') {
      // Bootstrap not loaded yet, retry after a short delay
      setTimeout(init, 50);
      return;
    }

    // Prevent dropdowns from auto-opening on navigation (only open on user click)
    preventAutoOpenDropdowns(navbar);

    // Handle navbar shrink on scroll
    updateNavbarOnScroll();

    // Update collapse position when opening
    collapse.addEventListener('show.bs.collapse', function() {
      updateCollapsePosition();
    });

    // Add/remove backdrop class when navbar opens/closes
    collapse.addEventListener('shown.bs.collapse', function() {
      navbar.classList.add('has-open-collapse');
      updateCollapsePosition(); // Update again after animation
    });

    collapse.addEventListener('hidden.bs.collapse', function() {
      navbar.classList.remove('has-open-collapse');
    });

    // Update position on window resize
    window.addEventListener('resize', function() {
      if (collapse.classList.contains('show')) {
        updateCollapsePosition();
      }
    });

    // Close on backdrop click (clicking outside navbar)
    document.addEventListener('click', function(e) {
      if (!collapse.classList.contains('show')) return;

      // Check if click is outside collapse and not on the toggler button
      if (!collapse.contains(e.target) &&
          !e.target.closest('.navbar-toggler')) {
        closeNavbar();
      }
    });

    // Close on nav link click (but NOT dropdown toggles)
    collapse.addEventListener('click', function(e) {
      // Close if clicking:
      // 1. A nav-link that is NOT a dropdown toggle
      // 2. A dropdown-item (menu item within dropdown)
      if ((e.target.matches('.nav-link') &&
           !e.target.matches('.dropdown-toggle') &&
           !e.target.closest('.dropdown-toggle')) ||
          e.target.matches('.dropdown-item')) {
        closeNavbar();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && collapse.classList.contains('show')) {
        closeNavbar();
      }
    });

    // Note: Bootstrap 5's default behavior is that dropdowns do NOT auto-open
    // when child items become active. They only open when the user clicks the toggle.
    // If dropdowns are auto-opening on navigation, check for custom code that might
    // be explicitly opening them.
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
