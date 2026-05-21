/**
 * UstaadJi Design Tokens
 * Premium dark theme with emerald accent for the informal economy brand.
 */

export const Colors = {
  // Core
  background: '#0A0E1A',
  surface: '#111827',
  surfaceLight: '#1F2937',
  surfaceGlass: 'rgba(31, 41, 55, 0.7)',

  // Accent — emerald green (trust, growth, Pakistan flag)
  primary: '#10B981',
  primaryLight: '#34D399',
  primaryDark: '#059669',
  primaryGlow: 'rgba(16, 185, 129, 0.15)',

  // Secondary — amber (warmth, informal economy, action)
  secondary: '#F59E0B',
  secondaryLight: '#FBBF24',

  // Text
  textPrimary: '#F9FAFB',
  textSecondary: '#9CA3AF',
  textMuted: '#6B7280',

  // Status
  success: '#10B981',
  error: '#EF4444',
  warning: '#F59E0B',

  // Chat bubbles
  userBubble: '#10B981',
  userBubbleText: '#FFFFFF',
  botBubble: '#1F2937',
  botBubbleText: '#F9FAFB',

  // Border
  border: 'rgba(75, 85, 99, 0.4)',
  borderLight: 'rgba(156, 163, 175, 0.2)',

  // Gradient stops
  gradientStart: '#10B981',
  gradientEnd: '#059669',

  // Shadows
  shadowColor: '#000000',
} as const;

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const Radius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  full: 9999,
} as const;

export const FontSize = {
  xs: 11,
  sm: 13,
  md: 15,
  lg: 17,
  xl: 20,
  xxl: 28,
  title: 34,
} as const;
