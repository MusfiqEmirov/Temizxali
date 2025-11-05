def normalize_az_phone(phone: str) -> str:
    """
    Azərbaycan mobil nömrəsini vahid formata salır.
    Məsələn:
      0512345678  →  994512345678
      +994512345678 →  994512345678
      512345678  →  994512345678
    """
    # Yalnız rəqəmləri saxla
    phone = ''.join(filter(str.isdigit, phone))

    # Əgər 0 ilə başlayırsa, onu sil
    if phone.startswith('0'):
        phone = phone[1:]

    # Əgər 994 ilə başlamırsa, əlavə et
    if not phone.startswith('994'):
        phone = '994' + phone

    return phone