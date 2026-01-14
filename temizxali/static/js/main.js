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
            $('.back-to-top').addClass('show');
        } else {
            $('.back-to-top').removeClass('show');
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


    // Testimonials carousel - Swiper.js
    $(document).ready(function() {
        if (document.querySelector('.testimonial-carousel')) {
            // Create navigation buttons in custom container before initializing Swiper
            var navContainer = document.querySelector('.testimonial-nav-container');
            if (navContainer && !navContainer.querySelector('.swiper-button-prev')) {
                navContainer.innerHTML = '<div class="swiper-button-prev"><i class="bi bi-chevron-left"></i></div><div class="swiper-button-next"><i class="bi bi-chevron-right"></i></div>';
            }
            
            var testimonialSwiper = new Swiper('.testimonial-carousel', {
                slidesPerView: 1,
                spaceBetween: 30,
                loop: true,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },
                speed: 1000,
                navigation: {
                    nextEl: '.testimonial-nav-container .swiper-button-next',
                    prevEl: '.testimonial-nav-container .swiper-button-prev',
                }
            });
        }
        
        // Service Images Carousel - Swiper.js
        if (document.querySelector('.service-images-carousel')) {
            // Create navigation buttons in custom container before initializing Swiper
            var serviceNavContainer = document.querySelector('.service-images-nav-container');
            if (serviceNavContainer && !serviceNavContainer.querySelector('.swiper-button-prev')) {
                serviceNavContainer.innerHTML = '<div class="swiper-button-prev"><i class="bi bi-chevron-left"></i></div><div class="swiper-button-next"><i class="bi bi-chevron-right"></i></div>';
            }
            
            var serviceImagesSwiper = new Swiper('.service-images-carousel', {
                slidesPerView: 1,
                spaceBetween: 15,
                loop: false,
                speed: 600,
                breakpoints: {
                    576: {
                        slidesPerView: 2,
                        spaceBetween: 15,
                    },
                    768: {
                        slidesPerView: 2,
                        spaceBetween: 20,
                    },
                    992: {
                        slidesPerView: 2,
                        spaceBetween: 20,
                    },
                    1200: {
                        slidesPerView: 3,
                        spaceBetween: 20,
                    }
                },
                navigation: {
                    nextEl: '.service-images-nav-container .swiper-button-next',
                    prevEl: '.service-images-nav-container .swiper-button-prev',
                }
            });
        }
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
    // Mobil üçün video həmişə oynasın
    var isMobile = window.innerWidth <= 768;
    
    if ('IntersectionObserver' in window) {
        var videoObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                var video = entry.target;
                // Mobil üçün video həmişə oynasın
                if (isMobile && video.classList.contains('video-bg')) {
                    if (video.paused && video.hasAttribute('autoplay')) {
                        video.play().catch(function() {
                            // Autoplay blocked, ignore
                        });
                    }
                    return; // Mobil üçün pause etmə
                }
                
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
            var video = this;
            // Mobil üçün video həmişə oynasın
            if (isMobile && $(video).hasClass('video-bg')) {
                if (video.paused && video.hasAttribute('autoplay')) {
                    video.play().catch(function() {
                        // Autoplay blocked, ignore
                    });
                }
            }
            videoObserver.observe(video);
        });
    }
    
    // Mobil üçün window resize zamanı yenidən yoxla
    $(window).on('resize', function() {
        isMobile = window.innerWidth <= 768;
        if (isMobile) {
            $('.service-item .video-bg').each(function() {
                var video = this;
                if (video.paused && video.hasAttribute('autoplay')) {
                    video.play().catch(function() {
                        // Autoplay blocked, ignore
                    });
                }
            });
        }
    });
    
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

// Language Switcher Toggle Script
document.addEventListener('DOMContentLoaded', function() {
    // Desktop language switcher
    const desktopSwitcher = document.querySelector('.language-switcher');
    const desktopBtn = document.querySelector('.language-btn-current');
    
    if (desktopBtn && desktopSwitcher) {
        desktopBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            desktopSwitcher.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!desktopSwitcher.contains(e.target)) {
                desktopSwitcher.classList.remove('active');
            }
        });
    }

    // Mobile language switcher
    const mobileSwitcher = document.querySelector('.language-switcher-mobile');
    const mobileBtn = document.querySelector('.language-btn-current-mobile');
    
    if (mobileBtn && mobileSwitcher) {
        mobileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileSwitcher.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileSwitcher.contains(e.target)) {
                mobileSwitcher.classList.remove('active');
            }
        });
    }

    // Carousel Auto-play
    var carouselElement = document.querySelector('#header-carousel');
    if (carouselElement) {
        var carousel = new bootstrap.Carousel(carouselElement, {
            interval: 5000,
            pause: false,
            wrap: true
        });
    }
});

// Lightbox X düyməsi üçün JavaScript - Bütün Lightbox-lar üçün (Projects, About, Services)
// Düymənin ölçüsü və yeri şəklin ölçüsünə görə tənzimlənir
$(document).ready(function() {
    // Container ölçüsünə görə düymə ölçüsünü hesabla
    function calculateButtonSize(containerWidth, containerHeight) {
        // Container-ın orta ölçüsünü götür
        var avgSize = (containerWidth + containerHeight) / 2;
        
        // Minimum və maksimum ölçülər
        var minSize = 35;
        var maxSize = 55;
        
        // Container ölçüsünə görə düymə ölçüsünü hesabla (container-ın 4%-i)
        var buttonSize = Math.max(minSize, Math.min(maxSize, avgSize * 0.04));
        
        // Yuvarlaqlaşdır
        return Math.round(buttonSize);
    }
    
    // Lightbox açıldıqda X düyməsi əlavə et
    function addCloseButton() {
        var $lightbox = $('#lightbox');
        var $imgContainer = $lightbox.find('.lb-container');
        
        if ($lightbox.length > 0 && $lightbox.is(':visible') && $('#lightbox-custom-close').length === 0 && $imgContainer.length > 0) {
            // Container ölçüsünü oxu
            var containerWidth = $imgContainer.width();
            var containerHeight = $imgContainer.height();
            
            // Container hələ ölçülməyibsə, bir az gözlə
            if (containerWidth === 0 || containerHeight === 0) {
                setTimeout(function() {
                    containerWidth = $imgContainer.width();
                    containerHeight = $imgContainer.height();
                    if (containerWidth > 0 && containerHeight > 0) {
                        createCloseButton($imgContainer, containerWidth, containerHeight);
                    }
                }, 100);
                return;
            }
            
            createCloseButton($imgContainer, containerWidth, containerHeight);
        }
    }
    
    // Düyməni yarat və yerləşdir
    function createCloseButton($imgContainer, containerWidth, containerHeight) {
        // Düymə ölçüsünü container ölçüsünə görə hesabla
        var buttonSize = calculateButtonSize(containerWidth, containerHeight);
        var fontSize = Math.round(buttonSize * 0.45);
        var iconSize = Math.round(buttonSize * 0.5);
        var offset = 5; // Container küncündən sabit 5px məsafə
        
        // Düyməni yarat
        var closeBtn = $('<button id="lightbox-custom-close"><i class="fas fa-times"></i></button>');
        
        // Şəklin ölçüsünə görə düyməni tənzimlə
        closeBtn.css({
            'position': 'absolute',
            'top': offset + 'px',
            'right': offset + 'px',
            'width': buttonSize + 'px',
            'height': buttonSize + 'px',
            'background': 'var(--primary)',
            'border-radius': '50%',
            'border': '2px solid rgba(255, 255, 255, 0.3)',
            'color': '#fff',
            'font-size': fontSize + 'px',
            'cursor': 'pointer',
            'z-index': '10001',
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'box-shadow': '0 2px 8px rgba(52, 142, 56, 0.4)',
            'transition': 'all 0.3s ease',
            'margin': '0',
            'padding': '0',
            'outline': 'none'
        });
        
        closeBtn.find('i').css({
            'font-size': iconSize + 'px',
            'line-height': '1'
        });
        
        $imgContainer.css('position', 'relative');
        $imgContainer.append(closeBtn);
        
        // X düyməsinə klik edəndə lightbox-ı bağla
        closeBtn.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (typeof lightbox !== 'undefined') {
                lightbox.end();
            }
            $(this).remove();
        });
        
        // Hover effekti
        closeBtn.on('mouseenter', function() {
            $(this).css({
                'background': '#2d7a31',
                'transform': 'scale(1.1)',
                'box-shadow': '0 4px 12px rgba(52, 142, 56, 0.6)'
            });
        }).on('mouseleave', function() {
            $(this).css({
                'background': 'var(--primary)',
                'transform': 'scale(1)',
                'box-shadow': '0 2px 8px rgba(52, 142, 56, 0.4)'
            });
        });
    }
    
    // Bütün lightbox link-lərinə klik edəndə (project-, about-gallery, service-gallery)
    $(document).on('click', 'a[data-lightbox]', function() {
        var attempts = 0;
        var checkInterval = setInterval(function() {
            attempts++;
            var $lightbox = $('#lightbox');
            var $imgContainer = $lightbox.find('.lb-container');
            if ($lightbox.length > 0 && $lightbox.is(':visible') && $imgContainer.length > 0) {
                addCloseButton();
                clearInterval(checkInterval);
            } else if (attempts > 40) {
                clearInterval(checkInterval);
            }
        }, 50);
    });
    
    // Lightbox DOM-a əlavə olunduqda (MutationObserver) - bütün lightbox-lar üçün
    var observer = new MutationObserver(function(mutations) {
        var $lightbox = $('#lightbox');
        var $imgContainer = $lightbox.find('.lb-container');
        
        if ($lightbox.length > 0 && $lightbox.is(':visible') && $imgContainer.length > 0) {
            // Container ölçüsü dəyişibsə və ya düymə yoxdursa
            if (!$('#lightbox-custom-close').length) {
                setTimeout(function() {
                    addCloseButton();
                }, 200);
            }
        } else if ($lightbox.length === 0 || !$lightbox.is(':visible')) {
            $('#lightbox-custom-close').remove();
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class', 'src']
    });
    
    // Container ölçüsü dəyişəndə düyməni yenilə
    var resizeTimer;
    $(window).on('resize', function() {
        var $lightbox = $('#lightbox');
        if ($lightbox.length > 0 && $lightbox.is(':visible')) {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                $('#lightbox-custom-close').remove();
                addCloseButton();
            }, 200);
        }
    });
    
    // Lightbox bağlandıqda X düyməsini sil
    $(document).on('click', '#lightboxOverlay', function() {
        $('#lightbox-custom-close').remove();
    });
    
    // ESC düyməsi ilə bağlandıqda da sil
    $(document).on('keydown', function(e) {
        if (e.keyCode === 27) {
            $('#lightbox-custom-close').remove();
        }
    });
});

// Floating Buttons JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const whatsappBtn = document.getElementById('whatsappBtn');
    const whatsappDropdown = document.getElementById('whatsappDropdown');
    
    if (whatsappBtn && whatsappDropdown) {
        // Toggle dropdown on button click
        whatsappBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            whatsappDropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!whatsappBtn.contains(e.target) && !whatsappDropdown.contains(e.target)) {
                whatsappDropdown.classList.remove('show');
            }
        });

        // Close dropdown when clicking on an option
        const whatsappOptions = whatsappDropdown.querySelectorAll('.whatsapp-option');
        whatsappOptions.forEach(function(option) {
            option.addEventListener('click', function() {
                whatsappDropdown.classList.remove('show');
            });
        });
    }
});