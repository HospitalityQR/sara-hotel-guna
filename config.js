/**
 * ============================================================================
 *  HOTEL THE SARA (गुना, मध्य प्रदेश) — CENTRAL BRAND & SECURITY CONFIGURATION
 * ============================================================================
 *  Stay in Style • Multi-Cuisine Luxury Dining, Banquets & Executive Stays
 *  AB Road, Near Kushmoda Chowki, Gaushala Mahaveerpura, Guna (M.P.)
 * ============================================================================
 */

window.RESTAURANT_CONFIG = {
    // 1. Brand Identity
    name: "Hotel The Sara",
    subname: "HOTEL THE SARA",
    tagline: "STAY IN STYLE • LUXURY DINING & BANQUETS",
    cityTagline: "AB ROAD • GUNA (M.P.)",
    highlight: "Multi-Cuisine Fine Dining • Royal Celebrations • Executive Rooms",
    diningHighlight: "Hygienic Family Dining • Grand Banquets • Premium Hospitality",

    // Primary Address & Location Details
    addressPrimaryLabel: "LOCATION",
    addressPrimary: "AB Road, Near Kushmoda Chowki, Gaushala Mahaveerpura, Guna, Madhya Pradesh 473001",
    city: "Guna, Madhya Pradesh",

    // Contact Numbers
    phone: "9303284300",
    phoneDisplay: "+91 93032 84300",
    altPhone: "7542268068",
    altPhoneDisplay: "+91 75422 68068",
    whatsapp: "9303284300",
    whatsappDisplay: "+91 93032 84300",
    whatsappUrl: "https://wa.me/919303284300?text=Namaste%20Hotel%20The%20Sara%2C%20I%20would%20like%20to%20connect%20for%20dining%20%2F%20room%20reservation.",

    // Brand Assets
    logoUrl: "logo_medallion.png",
    logoCleanUrl: "sara_logo_clean.png",
    bgUrl: "bg_ambience_brownish.jpg",

    // Ambience Showcase Photos
    ambiencePhotos: [
        "ambience_1.jpg?v=1",
        "ambience_2.jpg?v=1",
        "ambience_3.jpg?v=1"
    ],

    // 2. Exact Action Destination Links Provided by User
    // Google Review Link
    googleReviewUrl: "https://share.google/vRFMikseO8TDcpg9l",
    
    // Instagram Link & Handle
    instagramUrl: "https://www.instagram.com/hotelthesara?stkn=dzQwc3pzNGx0Y3Jo",
    instagramHandle: "@hotelthesara",

    // Hosted GitHub Pages URL
    landingPageUrl: "https://hospitalityqr.github.io/sara-hotel-guna/",

    // 3. Auto-Redirect Behavior
    autoRedirectToGoogle: false,
    autoRedirectDelayMs: 1200,

    // ========================================================================
    // 4. ANTI-COPY & DIGITAL LICENSE PROTECTION ENGINE (ANTI-THEFT LOCK)
    // ========================================================================
    license: {
        enabled: true,
        status: "ACTIVE", // Options: "ACTIVE", "LOCKED", "TRIAL"

        // Authorized Standee Identification
        authorizedStandeesCount: 1, // Number of authorized standees
        serialNumber: "HS-GUNA-VIP-001",
        tableNumber: "VIP TABLE #01",
        
        // Scan limit protection (Prevents 1 QR being duplicated across 20 tables)
        enableDailyScanLimit: true,
        maxDailyScans: 60,

        // Remote Kill-Switch message if duplicated without authorization
        lockTitle: "AUTHENTIC HARDWARE LICENSE VERIFICATION",
        lockMessage: "This Smart Hospitality Hub is registered for Single Table Display (#HS-GUNA-001). Multiple simultaneous scans detected. To activate multi-table dining service, contact your authorized provider.",
        vendorContact: "+91-XXXXXXXXXX (Authorized Provider)"
    }
};
