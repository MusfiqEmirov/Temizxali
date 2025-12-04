/**
 * Admin Panel Image Compress - Browser-də WebP-yə çevirir
 * Server RAM istifadə etmir - bütün iş browser-də olur
 */
(function() {
    'use strict';
    
    // jQuery-ni tap
    function getJQuery() {
        if (typeof django !== 'undefined' && django.jQuery) {
            return django.jQuery;
        }
        if (typeof jQuery !== 'undefined') {
            return jQuery;
        }
        if (typeof window.$ !== 'undefined' && typeof window.$.fn !== 'undefined' && typeof window.$.fn.jquery !== 'undefined') {
            return window.$;
        }
        return null;
    }
    
    // Script-i işə sal
    function startScript() {
        var $ = getJQuery();
        
        // Əgər jQuery yoxdursa, gözlə
        if (!$) {
            setTimeout(startScript, 100);
            return;
        }
        
        // jQuery-ni local scope-da saxla
        (function($) {
            console.log('[Image Compress] jQuery loaded, version:', $.fn.jquery);
            
            // WebP dəstəkləyirmi yoxla
            function supportsWebP() {
                try {
                    var canvas = document.createElement('canvas');
                    canvas.width = 1;
                    canvas.height = 1;
                    return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
                } catch (e) {
                    return false;
                }
            }

            if (!supportsWebP()) {
                console.warn('[Image Compress] Browser does not support WebP');
                return;
            }

            // Şəkil compress funksiyası
            function compressImageToWebP(file, maxWidth, maxHeight, quality) {
                return new Promise(function(resolve, reject) {
                    var reader = new FileReader();
                    
                    reader.onload = function(e) {
                        var img = new Image();
                        
                        img.onload = function() {
                            var canvas = document.createElement('canvas');
                            var width = img.width;
                            var height = img.height;
                            
                            // Ölçüləri hesabla (aspect ratio saxla)
                            if (width > maxWidth || height > maxHeight) {
                                var ratio = Math.min(maxWidth / width, maxHeight / height);
                                width = width * ratio;
                                height = height * ratio;
                            }
                            
                            canvas.width = width;
                            canvas.height = height;
                            
                            var ctx = canvas.getContext('2d');
                            ctx.drawImage(img, 0, 0, width, height);
                            
                            // WebP-yə çevir
                            canvas.toBlob(function(blob) {
                                if (blob) {
                                    var nameWithoutExt = file.name.replace(/\.[^/.]+$/, '');
                                    var webpName = nameWithoutExt + '.webp';
                                    
                                    var compressedFile = new File([blob], webpName, {
                                        type: 'image/webp',
                                        lastModified: Date.now()
                                    });
                                    resolve(compressedFile);
                                } else {
                                    reject(new Error('WebP conversion failed'));
                                }
                            }, 'image/webp', quality);
                        };
                        
                        img.onerror = function() {
                            reject(new Error('Image loading failed'));
                        };
                        
                        img.src = e.target.result;
                    };
                    
                    reader.onerror = function() {
                        reject(new Error('File reading failed'));
                    };
                    
                    reader.readAsDataURL(file);
                });
            }

            // Image field-ləri tap və işlə
            function initImageCompression() {
                $('input[type="file"]').each(function() {
                    var $input = $(this);
                    var inputName = $input.attr('name') || '';
                    var inputId = $input.attr('id') || '';
                    
                    // Yalnız image field-ləri
                    if (!inputName.toLowerCase().includes('image') && !inputId.toLowerCase().includes('image')) {
                        return;
                    }
                    
                    // Əgər artıq event listener var, təkrarlanmasın
                    if ($input.data('compression-initialized')) {
                        return;
                    }
                    
                    $input.data('compression-initialized', true);
                    console.log('[Image Compress] Initialized for:', inputName || inputId);
                    
                    $input.on('change', function(e) {
                        var file = e.target.files[0];
                        
                        if (!file) {
                            return;
                        }
                        
                        console.log('[Image Compress] File selected:', file.name, file.type, (file.size / 1024).toFixed(2) + ' KB');
                        
                        // Yalnız şəkil faylları
                        if (!file.type.match(/^image\//)) {
                            return;
                        }
                        
                        // Əgər artıq WebP-dirsə, dəyişmə
                        if (file.type === 'image/webp') {
                            console.log('[Image Compress] Already WebP, skipping');
                            return;
                        }
                        
                        // Progress göstər
                        var $progress = $input.siblings('.compress-progress');
                        if ($progress.length === 0) {
                            $progress = $('<div class="compress-progress" style="margin-top: 10px; padding: 10px; background: #e3f2fd; border-radius: 4px; border: 1px solid #2196f3;">' +
                                '<div style="font-weight: bold; margin-bottom: 5px; color: #1976d2;">🔄 Şəkil compress edilir...</div>' +
                                '<div class="compress-info" style="font-size: 12px; color: #666;"></div>' +
                                '</div>');
                            $input.after($progress);
                        }
                        
                        $progress.show();
                        $progress.find('.compress-info').text('Original ölçü: ' + (file.size / 1024).toFixed(2) + ' KB');
                        
                        // Async işlə
                        compressImageToWebP(file, 1920, 1080, 0.8).then(function(compressedFile) {
                            console.log('[Image Compress] Compression done:', compressedFile.name, (compressedFile.size / 1024).toFixed(2) + ' KB');
                            
                            // Yeni FileList yarat
                            var dataTransfer = new DataTransfer();
                            dataTransfer.items.add(compressedFile);
                            
                            // File input-u replace et
                            var nativeInput = $input[0];
                            nativeInput.files = dataTransfer.files;
                            
                            console.log('[Image Compress] File replaced. New file:', nativeInput.files[0].name, nativeInput.files[0].type);
                            
                            // Məlumat göstər
                            var originalSize = (file.size / 1024).toFixed(2);
                            var compressedSize = (compressedFile.size / 1024).toFixed(2);
                            var saved = ((1 - compressedFile.size / file.size) * 100).toFixed(1);
                            
                            $progress.find('.compress-info').html(
                                '✅ <strong>Compress tamamlandı!</strong><br>' +
                                'Original: ' + originalSize + ' KB → WebP: ' + compressedSize + ' KB<br>' +
                                'Qənaət: ' + saved + '% (' + ((file.size - compressedFile.size) / 1024).toFixed(2) + ' KB)'
                            );
                            
                            $progress.css({
                                'background': '#e8f5e9',
                                'border-color': '#4caf50'
                            });
                            
                            setTimeout(function() {
                                $progress.fadeOut();
                            }, 5000);
                        }).catch(function(error) {
                            console.error('[Image Compress] Error:', error);
                            $progress.find('.compress-info').html(
                                '❌ <strong>Xəta:</strong> ' + error.message + '<br>' +
                                'Original fayl istifadə olunacaq.'
                            );
                            $progress.css({
                                'background': '#ffebee',
                                'border-color': '#f44336'
                            });
                            setTimeout(function() {
                                $progress.fadeOut();
                            }, 5000);
                        });
                    });
                });
            }

            // Django admin ready - BÜTÜN KOD IIFE İÇİNDƏ
            $(document).ready(function() {
                console.log('[Image Compress] Script loaded');
                
                setTimeout(function() {
                    initImageCompression();
                }, 500);
                
                // Inline formlar üçün
                $(document).on('formset:added', function() {
                    setTimeout(function() {
                        initImageCompression();
                    }, 200);
                });
            });
            
        })($); // jQuery-ni parametr kimi ötürürük - scope təhlükəsizdir
    }
    
    // Script-i işə sal
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startScript);
    } else {
        startScript();
    }

})();

