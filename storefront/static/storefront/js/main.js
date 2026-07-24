(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.nav-bar').addClass('sticky-top shadow-sm');
        } else {
            $('.nav-bar').removeClass('sticky-top shadow-sm');
        }
    });


    // Hero Header carousel
    $(".header-carousel").owlCarousel({
        items: 1,
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: false,
        loop: true,
        margin: 0,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ]
    });


    // ProductList carousel
    $(".productList-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        dots: false,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="fas fa-chevron-left"></i>',
            '<i class="fas fa-chevron-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:2
            },
            1200:{
                items:3
            }
        }
    });

    // ProductList categories carousel
    $(".productImg-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        dots: false,
        loop: true,
        items: 1,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ]
    });


    // Single Products carousel
    $(".single-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        dots: true,
        dotsData: true,
        loop: true,
        items: 1,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ]
    });


    // ProductList carousel
    $(".related-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        dots: false,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="fas fa-chevron-left"></i>',
            '<i class="fas fa-chevron-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            },
            1200:{
                items:4
            }
        }
    });



    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });


    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


   

})(jQuery);


/* Fix for custom tab buttons and stretched links */
document.addEventListener("DOMContentLoaded", function() {
    // Tab switching fix for all custom tabs (.ptab, .pd-tab-btn, [data-bs-toggle="tab"])
    const tabButtons = document.querySelectorAll(".ptab, .pd-tab-btn, [data-bs-toggle='tab'], [data-bs-toggle='pill']");
    tabButtons.forEach(tab => {
        tab.addEventListener("click", function(e) {
            e.preventDefault();
            
            // Find container of tabs
            const tabList = this.closest('.pd-tabs, .product-tabs, .nav-tabs, [role="tablist"]') || this.parentElement.parentElement;
            
            if (tabList) {
                const siblings = tabList.querySelectorAll('.ptab, .pd-tab-btn, .nav-link, [data-bs-toggle="tab"], [data-bs-toggle="pill"]');
                siblings.forEach(t => {
                    t.classList.remove("active");
                    t.setAttribute("aria-selected", "false");
                });
            } else {
                tabButtons.forEach(t => t.classList.remove("active"));
            }
            
            this.classList.add("active");
            this.setAttribute("aria-selected", "true");
            
            // Hide all pane siblings or panes in tab-content
            const targetId = this.getAttribute("data-bs-target") || this.getAttribute("href");
            if (targetId && targetId.startsWith("#")) {
                const targetPane = document.querySelector(targetId);
                if (targetPane) {
                    const contentContainer = targetPane.closest(".tab-content") || targetPane.parentElement;
                    if (contentContainer) {
                        const panes = contentContainer.querySelectorAll(".tab-pane");
                        panes.forEach(p => p.classList.remove("show", "active"));
                    }
                    targetPane.classList.add("show", "active");
                }
            }
        });
    });

    // Auto-open tab on page load if URL has hash (e.g. #reviews or #nav-mission)
    const hash = window.location.hash;
    if (hash) {
        let targetTab = document.querySelector(`.pd-tab-btn[data-bs-target="${hash}"], .pd-tab-btn[href="${hash}"], [data-bs-target="${hash}"], ${hash}-tab`);
        if (hash === '#reviews' || hash === '#nav-mission') {
            targetTab = targetTab || document.getElementById('nav-mission-tab');
        }
        if (targetTab) {
            targetTab.click();
            setTimeout(() => {
                targetTab.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 200);
        }
    }
});
