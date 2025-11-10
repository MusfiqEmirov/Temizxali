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
    spinner();
    
    
    // WOW.js animasiyaları söndürülüb - heç bir effekt yoxdur
    // Bütün wow elementləri dərhal görünür
    $(document).ready(function() {
        $('.wow').css('visibility', 'visible');
    });


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
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


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Portfolio isotope and filter
    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');

        portfolioIsotope.isotope({filter: $(this).data('filter')});
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: false,
        loop: true,
        nav: true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });

    
})(jQuery);
document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('serviceSelectInput');
  const dropdown = document.getElementById('serviceDropdown');
  const checkboxes = dropdown.querySelectorAll('input[type="checkbox"]');

  // Aç/bağla funksiyası
  input.addEventListener('click', function (e) {
    e.stopPropagation();
    dropdown.classList.toggle('show');
  });

  // Seçilənləri input-a yazmaq
  checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      const selected = Array.from(checkboxes)
        .filter(c => c.checked)
        .map(c => {
          // Checkbox-un label-ını tap (xidmət adı)
          const label = c.closest('.form-check')?.querySelector('label.form-check-label');
          return label ? label.textContent.trim() : c.value;
        });
      input.value = selected.join(', ');
    });
  });

  // Çöldə klik ediləndə bağlansın
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.form-floating')) {
      dropdown.classList.remove('show');
    }
  });
});

// Lightbox optimizasiyası - sürətli yüklənmə və az loading ekranı
$(document).ready(function() {
    if (typeof lightbox !== 'undefined') {
        // Lightbox konfiqurasiyasını optimize et
        lightbox.option({
            'resizeDuration': 200,        // Container ölçüsü dəyişikliyi
            'fadeDuration': 200,           // Fade effekti
            'imageFadeDuration': 300,      // Şəkil fade effekti - flash-i aradan qaldırmaq üçün artırıldı
            'wrapAround': true,            // Son şəkildən birinciyə keçid
            'fitImagesInViewport': true,   // Şəkilləri viewport-a uyğunlaşdır
            'showImageNumberLabel': true,
            'alwaysShowNavOnTouchDevices': false
        });
        
        // Şəkilləri preload etmək üçün - səhifə yüklənəndə bütün gallery şəkillərini yüklə
        var preloadedImages = {};
        
        function preloadGalleryImages() {
            $('a[data-lightbox]').each(function() {
                var $link = $(this);
                var galleryName = $link.attr('data-lightbox');
                var imageUrl = $link.attr('href');
                
                if (galleryName && imageUrl && !preloadedImages[imageUrl]) {
                    var img = new Image();
                    img.onload = function() {
                        preloadedImages[imageUrl] = true;
                    };
                    img.src = imageUrl;
                    preloadedImages[imageUrl] = true; // Mark as loading
                }
            });
        }
        
        // Səhifə yüklənəndə şəkilləri preload et
        preloadGalleryImages();
        
        // Gallery açılanda qalan şəkilləri preload et
        $(document).on('click', 'a[data-lightbox]', function() {
            var galleryName = $(this).attr('data-lightbox');
            if (galleryName) {
                var $galleryLinks = $('a[data-lightbox="' + galleryName + '"]');
                $galleryLinks.each(function() {
                    var imageUrl = $(this).attr('href');
                    if (imageUrl && !preloadedImages[imageUrl]) {
                        var img = new Image();
                        img.src = imageUrl;
                        preloadedImages[imageUrl] = true;
                    }
                });
            }
        });
        
        // Flash problemini həll etmək üçün - Lightbox prototype metodlarını override et
        if (typeof lightbox !== 'undefined' && lightbox.constructor && lightbox.constructor.prototype) {
            var LightboxPrototype = lightbox.constructor.prototype;
            
            // Orijinal changeImage funksiyasını saxla
            var originalChangeImage = LightboxPrototype.changeImage;
            
            // changeImage funksiyasını override et - crossfade effekti
            LightboxPrototype.changeImage = function(imageNumber) {
                var self = this;
                var $image = this.$lightbox.find('.lb-image');
                var $container = this.$lightbox.find('.lb-container');
                
                // Köhnə şəkil varsa, yalnız opacity-ni azalt (hide etmə)
                if ($image.length && $image.attr('src') && $image.is(':visible')) {
                    // Köhnə şəkil fade-out (amma display: none etmə)
                    $image.stop(true, true).animate({
                        'opacity': 0
                    }, 200, function() {
                        // Opacity 0 olduqdan sonra orijinal funksiyanı çağır
                        originalChangeImage.call(self, imageNumber);
                    });
                } else {
                    // İlk dəfə açılanda və ya şəkil yoxdursa orijinal funksiyanı çağır
                    originalChangeImage.call(self, imageNumber);
                }
            };
            
            // showImage funksiyasını override et - smooth fade-in (crossfade)
            var originalShowImage = LightboxPrototype.showImage;
            LightboxPrototype.showImage = function() {
                var self = this;
                var $image = this.$lightbox.find('.lb-image');
                var imgSrc = $image.attr('src');
                
                // Loading-i gizlət
                this.$lightbox.find('.lb-loader').stop(true, true).hide();
                
                // Şəkil fade-in ilə göstər (crossfade effekti)
                if (imgSrc && $image.length) {
                    // Şəkil artıq DOM-da varsa, sadəcə opacity-ni artır
                    $image.css({
                        'opacity': '0',
                        'display': 'block',
                        'visibility': 'visible'
                    });
                    
                    // Preloaded şəkillər üçün daha sürətli fade-in
                    var fadeDuration = (preloadedImages[imgSrc]) ? 250 : 300;
                    
                    // Fade-in animasiyası
                    $image.stop(true, true).animate({
                        'opacity': 1
                    }, fadeDuration);
                } else {
                    $image.css('opacity', '1').show();
                }
                
                // Orijinal funksiyanın qalan hissəsini çağır
                this.updateNav();
                this.updateDetails();
                this.preloadNeighboringImages();
                this.enableKeyboardNav();
            };
        }
        
        // jQuery hide metodunu intercept et - .lb-image üçün display: none etmə
        var originalHide = $.fn.hide;
        $.fn.hide = function(speed, easing, callback) {
            // Əgər bu .lb-image-dirsə və lightbox içindədirsə, yalnız opacity-ni azalt
            if (this.hasClass('lb-image') && this.closest('#lightbox').length) {
                if (speed === undefined || typeof speed === 'function') {
                    // hide() çağırışı - yalnız opacity-ni azalt, display: none etmə
                    // Bu, crossfade effekti üçün vacibdir - şəkil heç vaxt tam gizlənməsin
                    return this.css({
                        'opacity': '0',
                        'visibility': 'hidden'
                    }).css('display', 'block'); // Display block qalsın
                } else {
                    // hide(speed) çağırışı - fadeOut istifadə et, amma display block qalsın
                    var $this = this;
                    return this.animate({
                        'opacity': 0
                    }, speed, easing, function() {
                        $this.css({
                            'visibility': 'hidden',
                            'display': 'block' // Display block qalsın
                        });
                        if (typeof callback === 'function') callback.call($this);
                    });
                }
            }
            // Digər elementlər üçün orijinal funksiyanı çağır
            return originalHide.apply(this, arguments);
        };
    }
});

// Service Detail Page Optimizasiyaları
$(document).ready(function() {
    // Image loading handlers - smooth fade-in
    function handleImageLoad(img) {
        if (img.complete && img.naturalHeight !== 0) {
            $(img).addClass('loaded');
        } else {
            $(img).on('load', function() {
                $(this).addClass('loaded');
            });
        }
    }
    
    // Service detail page images
    $('.service-main-image, .service-gallery-thumb, .related-service-image').each(function() {
        handleImageLoad(this);
    });
    
    // Intersection Observer for lazy loading optimization
    if ('IntersectionObserver' in window) {
        var imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    handleImageLoad(img);
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px'
        });
        
        // Observe lazy loaded images
        $('.service-gallery-thumb[loading="lazy"], .related-service-image[loading="lazy"]').each(function() {
            imageObserver.observe(this);
        });
    }
    
    // Video optimization - pause videos when not visible
    if ('IntersectionObserver' in window) {
        var videoObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                var video = entry.target;
                if (entry.isIntersecting) {
                    if (video.paused && video.hasAttribute('autoplay')) {
                        video.play().catch(function() {
                            // Autoplay blocked, ignore
                        });
                    }
                } else {
                    if (!video.paused) {
                        video.pause();
                    }
                }
            });
        }, {
            rootMargin: '100px'
        });
        
        $('.service-video, .video-bg').each(function() {
            videoObserver.observe(this);
        });
    }
    
    // Gallery thumbnail click optimization
    $('.service-gallery-thumb').on('click', function(e) {
        // Preload next/prev images for smoother navigation
        var $current = $(this).closest('.col-4, .col-md-3');
        var $next = $current.next();
        var $prev = $current.prev();
        
        if ($next.length) {
            var nextImg = new Image();
            nextImg.src = $next.find('a').attr('href');
        }
        if ($prev.length) {
            var prevImg = new Image();
            prevImg.src = $prev.find('a').attr('href');
        }
    });
    
    // Smooth scroll for related services
    $('.related-service-image').on('load', function() {
        $(this).addClass('loaded');
    });
    
    // Performance: Debounce scroll events
    var scrollTimeout;
    $(window).on('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            // Lazy load images in viewport
            $('.service-gallery-thumb[loading="lazy"], .related-service-image[loading="lazy"]').each(function() {
                var $img = $(this);
                if (isElementInViewport(this)) {
                    handleImageLoad(this);
                }
            });
        }, 100);
    });
    
    // Helper function to check if element is in viewport
    function isElementInViewport(el) {
        var rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
    
    // Preload critical images immediately
    $('.service-main-image').each(function() {
        handleImageLoad(this);
    });
});
