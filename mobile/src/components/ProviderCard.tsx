/**
 * ProviderCard — displays provider details on the booking confirmation screen.
 * Glassmorphism-inspired card with emerald accents.
 */
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors, Spacing, Radius, FontSize } from '../theme/colors';

interface Props {
  name: string;
  phone: string | null;
  category: string;
  bookingId: string;
  eta: string;
  bookedAt: string;
}

export default function ProviderCard({
  name,
  phone,
  category,
  bookingId,
  eta,
  bookedAt,
}: Props) {
  const categoryLabel = category.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <View style={styles.card}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.iconBg}>
          <Text style={styles.icon}>✅</Text>
        </View>
        <View style={styles.headerText}>
          <Text style={styles.statusText}>Booking Confirmed</Text>
          <Text style={styles.bookingId}>{bookingId}</Text>
        </View>
      </View>

      {/* Divider */}
      <View style={styles.divider} />

      {/* Provider Info */}
      <View style={styles.row}>
        <Text style={styles.label}>Provider</Text>
        <Text style={styles.value}>{name}</Text>
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Category</Text>
        <View style={styles.categoryBadge}>
          <Text style={styles.categoryText}>{categoryLabel}</Text>
        </View>
      </View>

      {phone && (
        <View style={styles.row}>
          <Text style={styles.label}>Phone</Text>
          <Text style={styles.value}>{phone}</Text>
        </View>
      )}

      <View style={styles.row}>
        <Text style={styles.label}>ETA</Text>
        <Text style={styles.valueHighlight}>{eta}</Text>
      </View>

      <View style={styles.row}>
        <Text style={styles.label}>Booked At</Text>
        <Text style={styles.value}>
          {new Date(bookedAt).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.surfaceGlass,
    borderRadius: Radius.xxl,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.lg,
    marginHorizontal: Spacing.md,
    // Shadow
    shadowColor: Colors.shadowColor,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.25,
    shadowRadius: 16,
    elevation: 8,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconBg: {
    width: 48,
    height: 48,
    borderRadius: Radius.full,
    backgroundColor: Colors.primaryGlow,
    alignItems: 'center',
    justifyContent: 'center',
  },
  icon: {
    fontSize: 24,
  },
  headerText: {
    marginLeft: Spacing.md,
  },
  statusText: {
    fontSize: FontSize.lg,
    fontWeight: '700',
    color: Colors.primary,
  },
  bookingId: {
    fontSize: FontSize.sm,
    color: Colors.textMuted,
    marginTop: 2,
  },
  divider: {
    height: 1,
    backgroundColor: Colors.border,
    marginVertical: Spacing.md,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: Spacing.sm,
  },
  label: {
    fontSize: FontSize.sm,
    color: Colors.textSecondary,
  },
  value: {
    fontSize: FontSize.md,
    color: Colors.textPrimary,
    fontWeight: '500',
  },
  valueHighlight: {
    fontSize: FontSize.md,
    color: Colors.secondary,
    fontWeight: '600',
  },
  categoryBadge: {
    backgroundColor: Colors.primaryGlow,
    paddingHorizontal: Spacing.sm + 2,
    paddingVertical: 3,
    borderRadius: Radius.full,
  },
  categoryText: {
    fontSize: FontSize.xs,
    color: Colors.primary,
    fontWeight: '600',
  },
});
