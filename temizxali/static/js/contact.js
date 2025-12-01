let addedServices = {};

// Translation helper function
function getTranslation(key) {
    const element = document.getElementById(`trans-${key}`);
    if (!element) {
        console.warn(`Translation element not found: trans-${key}`);
        return key;
    }
    const translation = element.textContent.trim();
    if (!translation) {
        console.warn(`Translation is empty for key: ${key}`);
        return key;
    }
    return translation;
}

function addService() {
    const selector = document.getElementById('serviceSelector');
    const selectedOption = selector.options[selector.selectedIndex];
    
    if (!selectedOption || !selectedOption.value) return;
    
    const serviceId = selectedOption.value;
    
    // Əgər bu xidmət artıq əlavə olunubsa, yenidən yaratma
    if (addedServices[serviceId]) {
        alert(getTranslation('service-already-added'));
        selector.value = '';
        return;
    }
    
    addedServices[serviceId] = true;
    
    const container = document.getElementById('servicesContainer');
    const serviceCard = createServiceCard(selectedOption);
    
    container.insertAdjacentHTML('beforeend', serviceCard);
    
    // Reset selector
    selector.value = '';
    
    // Add fade-in animation
    const lastCard = container.lastElementChild;
    if (lastCard) {
        lastCard.classList.add('fade-in');
    }
}

function createServiceCard(option) {
    const serviceId = option.value;
    const serviceName = option.getAttribute('data-service-name') || option.textContent.trim();
    const hasVariants = option.getAttribute('data-has-variants') === 'true';
    const priceStr = option.getAttribute('data-price') || '0';
    const vipPriceStr = option.getAttribute('data-vip-price') || '0';
    const premiumPriceStr = option.getAttribute('data-premium-price') || '0';
    const measureType = option.getAttribute('data-measure-type') || 'ədəd';
    const salesJson = option.getAttribute('data-sales') || '[]';
    
    const price = parseFloat(priceStr.replace(',', '.')) || 0;
    const vipPrice = parseFloat(vipPriceStr.replace(',', '.')) || 0;
    const premiumPrice = parseFloat(premiumPriceStr.replace(',', '.')) || 0;
    
    // Parse sales data
    let sales = [];
    try {
        let decodedJson = salesJson.replace(/&quot;/g, '"');
        decodedJson = decodedJson.replace(/(\d+),(\d+)/g, '$1.$2');
        sales = JSON.parse(decodedJson);
    } catch (e) {
        console.error('Sale məlumatları parse edilə bilmədi:', e);
        sales = [];
    }
    
    // Endirim badge-i göstərilməsin - yalnız hesablamada istifadə olunacaq
    
    // Unit placeholder müəyyən et based on measure_type
    let unitPlaceholder = getTranslation('value-placeholder');
    if (measureType === 'kg') {
        unitPlaceholder = getTranslation('value-placeholder-kg');
    } else if (measureType === 'm2') {
        unitPlaceholder = getTranslation('value-placeholder-m2');
    } else if (measureType === 'm') {
        unitPlaceholder = getTranslation('value-placeholder-m');
    } else if (measureType === 'ədəd') {
        unitPlaceholder = getTranslation('value-placeholder-unit');
    }

    // Variantlar varsa - dinamik versiya
    if (hasVariants) {
        // Variant məlumatlarını al
        const variantsJson = option.getAttribute('data-variants') || '[]';
        let variants = [];
        try {
            // HTML entity-ləri decode et (&quot; -> ")
            let decodedJson = variantsJson.replace(/&quot;/g, '"');
            // Vergülləri nöqtəyə çevir (JSON standartı üçün)
            decodedJson = decodedJson.replace(/(\d+),(\d+)/g, '$1.$2');
            variants = JSON.parse(decodedJson);
        } catch (e) {
            console.error('Variant məlumatları parse edilə bilmədi:', e);
            variants = [];
        }
        
        // Variantlar üçün HTML yarat
        let variantsHtml = '';
        if (variants.length > 0) {
            variantsHtml = `<div class="variant-container"><p class="fw-bold text-dark mb-3">${getTranslation('variants-label')}:</p>`;
            variants.forEach((variant, index) => {
                const variantId = variant.id;
                const variantName = variant.name || `${getTranslation('variant-default')} ${index + 1}`;
                const variantPrice = parseFloat(String(variant.price || 0).replace(',', '.')) || 0;
                const variantVipPrice = parseFloat(String(variant.vip_price || 0).replace(',', '.')) || 0;
                const variantPremiumPrice = parseFloat(String(variant.premium_price || 0).replace(',', '.')) || 0;
                
                variantsHtml += `
                    <div class="row g-2 mb-2 align-items-center">
                        <div class="col-auto">
                            <input class="form-check-input" type="checkbox" id="${serviceId}_variant_${variantId}_check"
                                onchange="toggleVariant('${serviceId}_variant_${variantId}')">
                        </div>
                        <div class="col-auto">
                            <label class="form-check-label fw-medium" for="${serviceId}_variant_${variantId}_check">${variantName}</label>
                        </div>
                        <div class="col-auto">
                            <select class="form-select form-select-sm" id="${serviceId}_variant_${variantId}_type" disabled onchange="calculateServicePrice('${serviceId}')">
                                <option value="normal">${getTranslation('normal')}</option>
                                ${variantVipPrice > 0 ? `<option value="vip">${getTranslation('vip')}</option>` : ''}
                                ${variantPremiumPrice > 0 ? `<option value="premium">${getTranslation('premium')}</option>` : ''}
                            </select>
                        </div>
                        <div class="col">
                            <input type="text" class="form-control form-control-sm" id="${serviceId}_variant_${variantId}_value"
                                placeholder="${unitPlaceholder}" disabled
                                oninput="this.value = this.value.replace(/[^0-9.]/g, ''); calculateServicePrice('${serviceId}')">
                        </div>
                    </div>
                `;
            });
            variantsHtml += '</div>';
        }
        
        return `
            <div class="service-card" id="${serviceId}" data-service-id="${serviceId}">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div class="service-title">
                        ${serviceName}
                    </div>
                    <button class="btn-remove" onclick="removeService('${serviceId}')">
                        <i class="fas fa-times"></i> ${getTranslation('remove')}
                    </button>
                </div>

                ${variantsHtml}
                
                <div class="alert alert-info mt-3" id="${serviceId}_price_final" style="display: none;">
                    <strong>${getTranslation('price')}:</strong> <span id="${serviceId}_price_amount_final">0.00 ₼</span>
                </div>
            </div>
        `;
    } else {
        // Variantlar yoxdursa
        return `
            <div class="service-card" id="${serviceId}" data-service-id="${serviceId}">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div class="service-title">
                        ${serviceName}
                    </div>
                    <button class="btn-remove" onclick="removeService('${serviceId}')">
                        <i class="fas fa-times"></i> ${getTranslation('remove')}
                    </button>
                </div>
                
                <div class="row g-2">
                    <div class="col-auto">
                        <select class="form-select" id="${serviceId}_type" onchange="calculateServicePrice('${serviceId}')">
                            <option value="normal">${getTranslation('normal')}</option>
                            ${vipPrice > 0 ? `<option value="vip">${getTranslation('vip')}</option>` : ''}
                            ${premiumPrice > 0 ? `<option value="premium">${getTranslation('premium')}</option>` : ''}
                        </select>
                    </div>
                    <div class="col">
                        <input type="text" class="form-control" id="${serviceId}_value"
                            placeholder="${unitPlaceholder}"
                            oninput="this.value = this.value.replace(/[^0-9.]/g, ''); calculateServicePrice('${serviceId}')">
                    </div>
                </div>
                
                <div class="alert alert-info mt-3" id="${serviceId}_price" style="display: none;">
                    <strong>${getTranslation('price')}:</strong> <span id="${serviceId}_price_amount">0.00 ₼</span>
                </div>
            </div>
        `;
    }
}

function removeService(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
        delete addedServices[id];
        calculateTotal();
    }
}

function toggleVariant(variantId) {
    const checkbox = document.getElementById(variantId + '_check');
    const select = document.getElementById(variantId + '_type');
    const input = document.getElementById(variantId + '_value');
    
    if (!checkbox || !select || !input) return;
    
    select.disabled = !checkbox.checked;
    input.disabled = !checkbox.checked;
    
    if (!checkbox.checked) {
        input.value = '';
    }
    
    // Extract service ID from variant ID (format: serviceId_variant_variantId)
    const parts = variantId.split('_variant_');
    if (parts.length === 2) {
        const serviceId = parts[0];
        calculateServicePrice(serviceId);
    }
}

function calculateServicePrice(serviceId) {
    const card = document.getElementById(serviceId);
    if (!card) return;
    
    const option = document.querySelector(`#serviceSelector option[value="${serviceId}"]`);
    if (!option) return;
    
    const priceStr = option.getAttribute('data-price') || '0';
    const vipPriceStr = option.getAttribute('data-vip-price') || '0';
    const premiumPriceStr = option.getAttribute('data-premium-price') || '0';
    const measureType = option.getAttribute('data-measure-type') || 'ədəd';
    const salesJson = option.getAttribute('data-sales') || '[]';
    
    const price = parseFloat(priceStr.replace(',', '.')) || 0;
    const vipPrice = parseFloat(vipPriceStr.replace(',', '.')) || 0;
    const premiumPrice = parseFloat(premiumPriceStr.replace(',', '.')) || 0;
    
    // Parse sales data
    let sales = [];
    try {
        let decodedJson = salesJson.replace(/&quot;/g, '"');
        decodedJson = decodedJson.replace(/(\d+),(\d+)/g, '$1.$2');
        sales = JSON.parse(decodedJson);
    } catch (e) {
        console.error('Sale məlumatları parse edilə bilmədi:', e);
        sales = [];
    }
    
    // Helper function to get applicable discount based on min_quantity
    function getApplicableDiscount(value) {
        // Find applicable sale event - SaleEvent service-ə bağlıdır, ona görə də service-in measure_type-ı ilə uyğun olur
        let applicableSale = null;
        for (let sale of sales) {
            if (sale.active && parseFloat(value) >= parseFloat(sale.min_quantity || 0)) {
                if (!applicableSale || parseFloat(sale.sale || 0) > parseFloat(applicableSale.sale || 0)) {
                    applicableSale = sale;
                }
            }
        }
        
        return applicableSale ? parseFloat(applicableSale.sale || 0) : 0;
    }
    
    let serviceTotal = 0;
    
    // Variantlar hesablaması (dinamik)
    const variantsJson = option.getAttribute('data-variants') || '[]';
    let variants = [];
    try {
        // HTML entity-ləri decode et (&quot; -> ")
        let decodedJson = variantsJson.replace(/&quot;/g, '"');
        // Vergülləri nöqtəyə çevir (JSON standartı üçün)
        decodedJson = decodedJson.replace(/(\d+),(\d+)/g, '$1.$2');
        variants = JSON.parse(decodedJson);
    } catch (e) {
        console.error('Variant məlumatları parse edilə bilmədi:', e);
        variants = [];
    }
    
    // Əgər variantlar varsa, əsas xidmət hesablamasını skip et
    const hasVariants = variants.length > 0;
    
    if (!hasVariants) {
        // Əsas xidmət hesablaması (yalnız variantlar yoxdursa)
        const value = parseFloat(document.getElementById(`${serviceId}_value`)?.value) || 0;
        const priceType = document.getElementById(`${serviceId}_type`)?.value || 'normal';
        
        let basePrice = 0;
        if (priceType === 'vip' && vipPrice > 0) {
            basePrice = vipPrice;
        } else if (priceType === 'premium' && premiumPrice > 0) {
            basePrice = premiumPrice;
        } else {
            basePrice = price;
        }
        
        if (value > 0 && basePrice > 0) {
            let calculated = 0;
            if (measureType === 'kg' || measureType === 'm2' || measureType === 'm' || measureType === 'ədəd') {
                calculated = basePrice * value;
            } else {
                calculated = basePrice;
            }
            
            // Endirim tətbiq et - yalnız value >= min_quantity olduqda
            const discountPercent = getApplicableDiscount(value);
            const discountAmount = (calculated * discountPercent) / 100;
            serviceTotal += calculated - discountAmount;
        }
    } else {
        // Variantlar varsa - əvvəlcə bütün variantların cəmini hesabla
        let totalVariantValue = 0;
        variants.forEach((variant) => {
            const variantId = variant.id;
            const variantCheck = document.getElementById(`${serviceId}_variant_${variantId}_check`);
            if (variantCheck && variantCheck.checked) {
                const variantValue = parseFloat(document.getElementById(`${serviceId}_variant_${variantId}_value`)?.value) || 0;
                totalVariantValue += variantValue;
            }
        });
        
        // Variantların cəminə əsasən endirim faizini tap
        const discountPercent = getApplicableDiscount(totalVariantValue);
        
        // İndi hər variant üçün hesabla və endirimi tətbiq et
        variants.forEach((variant) => {
            const variantId = variant.id;
            const variantCheck = document.getElementById(`${serviceId}_variant_${variantId}_check`);
            if (variantCheck && variantCheck.checked) {
                const variantValue = parseFloat(document.getElementById(`${serviceId}_variant_${variantId}_value`)?.value) || 0;
                const variantPriceType = document.getElementById(`${serviceId}_variant_${variantId}_type`)?.value || 'normal';
                
                // Dinamik qiymətlər
                let variantBasePrice = 0;
                if (variantPriceType === 'vip') {
                    variantBasePrice = parseFloat(String(variant.vip_price || 0).replace(',', '.')) || 0;
                } else if (variantPriceType === 'premium') {
                    variantBasePrice = parseFloat(String(variant.premium_price || 0).replace(',', '.')) || 0;
                } else {
                    variantBasePrice = parseFloat(String(variant.price || 0).replace(',', '.')) || 0;
                }
                
                if (variantValue > 0 && variantBasePrice > 0) {
                    let variantCalculated = 0;
                    if (measureType === 'kg' || measureType === 'm2' || measureType === 'm' || measureType === 'ədəd') {
                        variantCalculated = variantBasePrice * variantValue;
                    } else {
                        variantCalculated = variantBasePrice;
                    }
                    
                    // Endirim tətbiq et - variantların cəminə əsasən
                    const variantDiscountAmount = (variantCalculated * discountPercent) / 100;
                    serviceTotal += variantCalculated - variantDiscountAmount;
                }
            }
        });
    }
    
    // Xidmət qiymətini göstər
    // Variantlar olan service-lər üçün _price_final, digərləri üçün _price
    const priceDiv = document.getElementById(hasVariants ? `${serviceId}_price_final` : `${serviceId}_price`);
    const priceAmount = document.getElementById(hasVariants ? `${serviceId}_price_amount_final` : `${serviceId}_price_amount`);
    
    if (priceDiv && priceAmount) {
        if (serviceTotal > 0) {
            // Endirim faizini hesabla və göstər - yalnız dəyər daxil edildikdə
            let discountInfo = '';
            if (!hasVariants) {
                // Əsas xidmət üçün
                const value = parseFloat(document.getElementById(`${serviceId}_value`)?.value) || 0;
                if (value > 0) {
                    const discountPercent = getApplicableDiscount(value);
                    if (discountPercent > 0) {
                        discountInfo = ` <span class="text-success small">(-${discountPercent.toFixed(0)}%)</span>`;
                    }
                }
            } else {
                // Variantlar üçün - variantların cəminə əsasən endirim faizini tap
                let totalVariantValue = 0;
                variants.forEach((variant) => {
                    const variantId = variant.id;
                    const variantCheck = document.getElementById(`${serviceId}_variant_${variantId}_check`);
                    if (variantCheck && variantCheck.checked) {
                        const variantValue = parseFloat(document.getElementById(`${serviceId}_variant_${variantId}_value`)?.value) || 0;
                        totalVariantValue += variantValue;
                    }
                });
                if (totalVariantValue > 0) {
                    const discountPercent = getApplicableDiscount(totalVariantValue);
                    if (discountPercent > 0) {
                        discountInfo = ` <span class="text-success small">(-${discountPercent.toFixed(0)}%)</span>`;
                    }
                }
            }
            priceAmount.innerHTML = serviceTotal.toFixed(2) + ' ₼' + discountInfo;
            priceDiv.style.display = 'block';
        } else {
            priceDiv.style.display = 'none';
        }
    }
}

function calculateTotal() {
    let total = 0;

    Object.keys(addedServices).forEach(serviceId => {
        const option = document.querySelector(`#serviceSelector option[value="${serviceId}"]`);
        if (!option) return;
        
        const priceStr = option.getAttribute('data-price') || '0';
        const vipPriceStr = option.getAttribute('data-vip-price') || '0';
        const premiumPriceStr = option.getAttribute('data-premium-price') || '0';
        const measureType = option.getAttribute('data-measure-type') || 'ədəd';
        const salesJson = option.getAttribute('data-sales') || '[]';
        
        const price = parseFloat(priceStr.replace(',', '.')) || 0;
        const vipPrice = parseFloat(vipPriceStr.replace(',', '.')) || 0;
        const premiumPrice = parseFloat(premiumPriceStr.replace(',', '.')) || 0;
        
        // Parse sales data
        let sales = [];
        try {
            let decodedJson = salesJson.replace(/&quot;/g, '"');
            decodedJson = decodedJson.replace(/(\d+),(\d+)/g, '$1.$2');
            sales = JSON.parse(decodedJson);
        } catch (e) {
            console.error('Sale məlumatları parse edilə bilmədi:', e);
            sales = [];
        }
        
        // Helper function to get applicable discount based on min_quantity
        function getApplicableDiscount(value) {
            // Find applicable sale event - SaleEvent service-ə bağlıdır, ona görə də service-in measure_type-ı ilə uyğun olur
            let applicableSale = null;
            for (let sale of sales) {
                if (sale.active && parseFloat(value) >= parseFloat(sale.min_quantity || 0)) {
                    if (!applicableSale || parseFloat(sale.sale || 0) > parseFloat(applicableSale.sale || 0)) {
                        applicableSale = sale;
                    }
                }
            }
            
            return applicableSale ? parseFloat(applicableSale.sale || 0) : 0;
        }
        
        // Variantlar hesablaması (dinamik)
        const variantsJson = option.getAttribute('data-variants') || '[]';
        let variants = [];
        try {
            // HTML entity-ləri decode et (&quot; -> ")
            let decodedJson = variantsJson.replace(/&quot;/g, '"');
            // Vergülləri nöqtəyə çevir (JSON standartı üçün)
            decodedJson = decodedJson.replace(/(\d+),(\d+)/g, '$1.$2');
            variants = JSON.parse(decodedJson);
        } catch (e) {
            console.error('Variant məlumatları parse edilə bilmədi:', e);
            variants = [];
        }
        
        // Əgər variantlar varsa, əsas xidmət hesablamasını skip et
        const hasVariants = variants.length > 0;
        
        if (!hasVariants) {
            // Əsas xidmət hesablaması (yalnız variantlar yoxdursa)
            const value = parseFloat(document.getElementById(`${serviceId}_value`)?.value) || 0;
            const priceType = document.getElementById(`${serviceId}_type`)?.value || 'normal';
            
            let basePrice = 0;
            if (priceType === 'vip' && vipPrice > 0) {
                basePrice = vipPrice;
            } else if (priceType === 'premium' && premiumPrice > 0) {
                basePrice = premiumPrice;
            } else {
                basePrice = price;
            }
            
            if (value > 0 && basePrice > 0) {
                let calculated = 0;
                if (measureType === 'kg' || measureType === 'm2' || measureType === 'm' || measureType === 'ədəd') {
                    calculated = basePrice * value;
                } else {
                    calculated = basePrice;
                }
                
                // Endirim tətbiq et - yalnız value >= min_quantity olduqda
                const discountPercent = getApplicableDiscount(value);
                const discountAmount = (calculated * discountPercent) / 100;
                total += calculated - discountAmount;
            }
        } else {
            // Variantlar varsa - əvvəlcə bütün variantların cəmini hesabla
            let totalVariantValue = 0;
            variants.forEach((variant) => {
                const variantId = variant.id;
                const variantCheck = document.getElementById(`${serviceId}_variant_${variantId}_check`);
                if (variantCheck && variantCheck.checked) {
                    const variantValue = parseFloat(document.getElementById(`${serviceId}_variant_${variantId}_value`)?.value) || 0;
                    totalVariantValue += variantValue;
                }
            });
            
            // Variantların cəminə əsasən endirim faizini tap
            const discountPercent = getApplicableDiscount(totalVariantValue);
            
            // İndi hər variant üçün hesabla və endirimi tətbiq et
            variants.forEach((variant) => {
                const variantId = variant.id;
                const variantCheck = document.getElementById(`${serviceId}_variant_${variantId}_check`);
                if (variantCheck && variantCheck.checked) {
                    const variantValue = parseFloat(document.getElementById(`${serviceId}_variant_${variantId}_value`)?.value) || 0;
                    const variantPriceType = document.getElementById(`${serviceId}_variant_${variantId}_type`)?.value || 'normal';
                    
                    // Dinamik qiymətlər
                    let variantBasePrice = 0;
                    if (variantPriceType === 'vip') {
                        variantBasePrice = parseFloat(variant.vip_price) || 0;
                    } else if (variantPriceType === 'premium') {
                        variantBasePrice = parseFloat(variant.premium_price) || 0;
                    } else {
                        variantBasePrice = parseFloat(variant.price) || 0;
                    }
                    
                    if (variantValue > 0 && variantBasePrice > 0) {
                        let variantCalculated = 0;
                        if (measureType === 'kg' || measureType === 'm2' || measureType === 'm' || measureType === 'ədəd') {
                            variantCalculated = variantBasePrice * variantValue;
                        } else {
                            variantCalculated = variantBasePrice;
                        }
                        
                        // Endirim tətbiq et - variantların cəminə əsasən
                        const variantDiscountAmount = (variantCalculated * discountPercent) / 100;
                        total += variantCalculated - variantDiscountAmount;
                    }
                }
            });
        }
    });

    // Nəticəni göstər
    const resultCard = document.getElementById('resultCard');
    const totalAmount = document.getElementById('totalAmount');
    
    if (resultCard && totalAmount) {
        if (total > 0) {
            // Ümumi endirim faizini hesabla (bütün servislər üçün)
            let totalDiscountInfo = '';
            // Burada ümumi endirim faizini hesablamaq çətindir, ona görə də sadəcə məbləği göstəririk
            // Əgər lazımdırsa, hər service üçün endirim faizini ayrı-ayrı göstərmək olar
            totalAmount.textContent = total.toFixed(2) + ' ₼';
            resultCard.style.display = 'block';
            resultCard.classList.add('fade-in');
        } else {
            resultCard.style.display = 'none';
        }
    }
}

// Order mesajını anlıq göstər
document.addEventListener('DOMContentLoaded', function() {
    const orderMessage = document.getElementById('orderMessage');
    if (orderMessage) {
        // Scroll to message
        orderMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Highlight effect
        orderMessage.style.transform = 'scale(1.02)';
        orderMessage.style.transition = 'transform 0.3s ease-out';
        setTimeout(function() {
            orderMessage.style.transform = 'scale(1)';
        }, 300);
        
        // Auto-hide after 5 seconds (optional)
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(orderMessage);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    }
});

