---
name: Gilded Serenity
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#37393a'
  surface-container-lowest: '#0c0f0f'
  surface-container-low: '#1a1c1c'
  surface-container: '#1e2020'
  surface-container-high: '#282a2b'
  surface-container-highest: '#333535'
  on-surface: '#e2e2e2'
  on-surface-variant: '#d0c5af'
  inverse-surface: '#e2e2e2'
  inverse-on-surface: '#2f3131'
  outline: '#99907c'
  outline-variant: '#4d4635'
  surface-tint: '#e9c349'
  primary: '#f2ca50'
  on-primary: '#3c2f00'
  primary-container: '#d4af37'
  on-primary-container: '#554300'
  inverse-primary: '#735c00'
  secondary: '#c8c6c5'
  on-secondary: '#313030'
  secondary-container: '#474746'
  on-secondary-container: '#b7b5b4'
  tertiary: '#f1c97d'
  on-tertiary: '#412d00'
  tertiary-container: '#d3ad65'
  on-tertiary-container: '#5b4000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffe088'
  primary-fixed-dim: '#e9c349'
  on-primary-fixed: '#241a00'
  on-primary-fixed-variant: '#574500'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#ffdea5'
  tertiary-fixed-dim: '#e9c176'
  on-tertiary-fixed: '#261900'
  on-tertiary-fixed-variant: '#5d4201'
  background: '#121414'
  on-background: '#e2e2e2'
  surface-variant: '#333535'
typography:
  headline-xl:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-md:
    fontFamily: Playfair Display
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-lg:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-padding-mobile: 20px
  container-padding-desktop: 64px
  gutter: 24px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style
The design system is centered on the concept of "Atmospheric Luxury." It targets a high-end demographic seeking both prestige and comfort. The visual language balances the weight of deep, dark foundations with the lightness of gold accents and ethereal glassmorphism.

The style is a hybrid of **Minimalism** and **Glassmorphism**. It utilizes expansive, high-quality lifestyle photography as a backdrop, with UI elements acting as translucent "veils" that provide information without severing the connection to the physical space of the hotel. The emotional response is one of calm, exclusivity, and warm hospitality.

## Colors
The palette is rooted in deep, matte blacks and charcoals to establish a premium foundation. 

- **Primary (Gold/Copper):** Used sparingly for high-intent actions, highlights, and critical branding elements to evoke warmth and value.
- **Secondary (Charcoal):** The core surface color, typically applied with varying levels of opacity to create depth.
- **Neutral (White):** Reserved for primary typography and iconography to ensure maximum legibility against dark backgrounds.
- **Translucency:** Surface colors should use an alpha channel (e.g., `rgba(26, 26, 26, 0.8)`) to allow background photography to bleed through subtly.

## Typography
This design system employs a classic high-contrast pairing. **Playfair Display** provides an editorial, sophisticated feel for headings, reflecting the "Our Menu" and logo aesthetic. **Manrope** offers a clean, highly legible, and modern counterpoint for all functional and body text. 

For labels and small buttons, use uppercase Manrope with increased letter spacing to maintain an "expensive" feel. Headline tracking should be slightly tightened to feel more cohesive.

## Layout & Spacing
The layout follows a **Fluid Grid** model with generous safe areas to maintain a sense of "breathability" and luxury. 

- **Mobile:** 4-column grid with 20px side margins. Elements typically stack vertically.
- **Tablet:** 8-column grid with 40px side margins.
- **Desktop:** 12-column grid with a maximum content width of 1440px. 

Spacing follows an 8px rhythmic scale. Use larger "stack" values (48px+) between major sections to prevent the UI from feeling crowded. Content should be centered or aligned to the left with significant whitespace to emphasize the background imagery.

## Elevation & Depth
Depth is achieved through **Glassmorphism** rather than traditional drop shadows. 

1.  **Base Layer:** Full-screen photography with a subtle dark overlay (20-40% opacity).
2.  **Surface Layer:** Backgrounds of cards and menus use a 70-85% opaque charcoal with a background blur (15px to 25px).
3.  **Accent Layer:** Active elements or primary buttons use solid colors or subtle gradients to "pop" off the translucent surfaces.

Borders should be "Ghost Borders"—1px solid lines with low opacity (white at 10-15%) to define edges without adding visual weight.

## Shapes
The shape language is "Softly Geometric." All containers, cards, and buttons use a consistent 0.5rem (8px) radius. This provides a modern, approachable feel that avoids the clinical nature of sharp corners or the overly casual nature of full pills. Larger cards (like room previews or menu sections) should scale up to `rounded-xl` (24px) to emphasize their container status.

## Components
- **Buttons:** Primary buttons are solid Gold/Copper with black text. Secondary buttons are outlined (Ghost) with white text.
- **Cards:** Use the Glassmorphism style defined in the Elevation section. Images within cards should have a slight zoom-in effect on hover.
- **Input Fields:** Bottom-border only or very light ghost-outlined boxes. Focus states should transition the border color to Gold.
- **Chips/Badges:** Small, translucent dark pills with Gold text for labels like "Luxury Suite" or "Available."
- **Navigation:** A top-aligned transparent bar that becomes a blurred charcoal strip upon scrolling.
- **Lists:** Clean, separated by 1px low-opacity white dividers. Icons in lists should be thin-stroke (Linear) and Gold.
- **Specialty Component - "The Curator":** A floating booking bar at the bottom of the screen that remains docked, using a high-blur glass effect to stay visible over any background.