/**
 * BookingScreen — Displays the booking confirmation after a provider is dispatched.
 *
 * Navigated to from ChatScreen (or future provider list).
 * Shows a ProviderCard with all booking details and a success animation.
 */
import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  SafeAreaView,
  StatusBar,
  ScrollView,
} from 'react-native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RouteProp } from '@react-navigation/native';
import ProviderCard from '../components/ProviderCard';
import { Colors, Spacing, Radius, FontSize } from '../theme/colors';

type RootStackParamList = {
  Chat: undefined;
  Booking: {
    bookingId: string;
    providerName: string;
    providerPhone: string | null;
    providerCategory: string;
    eta: string;
    bookedAt: string;
    message: string;
  };
};

interface Props {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Booking'>;
  route: RouteProp<RootStackParamList, 'Booking'>;
}

export default function BookingScreen({ navigation, route }: Props) {
  const {
    bookingId,
    providerName,
    providerPhone,
    providerCategory,
    eta,
    bookedAt,
    message,
  } = route.params;

  const scaleAnim = useRef(new Animated.Value(0)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.sequence([
      Animated.spring(scaleAnim, {
        toValue: 1,
        tension: 60,
        friction: 8,
        useNativeDriver: true,
      }),
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar barStyle="light-content" backgroundColor={Colors.background} />

      {/* ── Header ───────────────────────────────────────────────── */}
      <View style={styles.header}>
        <TouchableOpacity
          onPress={() => navigation.goBack()}
          style={styles.backBtn}
        >
          <Text style={styles.backIcon}>←</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Booking Confirmation</Text>
        <View style={{ width: 36 }} />
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* ── Success Animation ──────────────────────────────────── */}
        <Animated.View
          style={[
            styles.successContainer,
            { transform: [{ scale: scaleAnim }] },
          ]}
        >
          <View style={styles.checkCircle}>
            <Text style={styles.checkMark}>✓</Text>
          </View>
          <Text style={styles.successTitle}>Shukriya! 🎉</Text>
          <Text style={styles.successSub}>
            Aapka ustaad raste mein hai
          </Text>
        </Animated.View>

        {/* ── Provider Card ──────────────────────────────────────── */}
        <Animated.View style={{ opacity: fadeAnim }}>
          <ProviderCard
            name={providerName}
            phone={providerPhone}
            category={providerCategory}
            bookingId={bookingId}
            eta={eta}
            bookedAt={bookedAt}
          />

          {/* ── Message from backend ────────────────────────────── */}
          <View style={styles.messageCard}>
            <Text style={styles.messageLabel}>📋 Details</Text>
            <Text style={styles.messageText}>{message}</Text>
          </View>

          {/* ── Back to Chat Button ─────────────────────────────── */}
          <TouchableOpacity
            style={styles.backToChatBtn}
            onPress={() => navigation.navigate('Chat')}
            activeOpacity={0.8}
          >
            <Text style={styles.backToChatText}>💬 Chat par wapas jayein</Text>
          </TouchableOpacity>
        </Animated.View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: Colors.background,
  },

  // Header
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm + 4,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  backBtn: {
    width: 36,
    height: 36,
    borderRadius: Radius.full,
    backgroundColor: Colors.surfaceLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  backIcon: {
    fontSize: 20,
    color: Colors.textPrimary,
  },
  headerTitle: {
    fontSize: FontSize.lg,
    fontWeight: '700',
    color: Colors.textPrimary,
  },

  scrollContent: {
    paddingBottom: Spacing.xxl,
  },

  // Success
  successContainer: {
    alignItems: 'center',
    paddingVertical: Spacing.xl,
  },
  checkCircle: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: Colors.primaryGlow,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: Spacing.md,
    borderWidth: 2,
    borderColor: Colors.primary,
  },
  checkMark: {
    fontSize: 36,
    color: Colors.primary,
    fontWeight: '700',
  },
  successTitle: {
    fontSize: FontSize.xxl,
    fontWeight: '800',
    color: Colors.textPrimary,
    marginBottom: 4,
  },
  successSub: {
    fontSize: FontSize.md,
    color: Colors.textSecondary,
  },

  // Message card
  messageCard: {
    backgroundColor: Colors.surfaceGlass,
    borderRadius: Radius.lg,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
    marginHorizontal: Spacing.md,
    marginTop: Spacing.md,
  },
  messageLabel: {
    fontSize: FontSize.sm,
    color: Colors.textMuted,
    marginBottom: Spacing.sm,
    fontWeight: '600',
  },
  messageText: {
    fontSize: FontSize.md,
    color: Colors.textPrimary,
    lineHeight: 22,
  },

  // CTA
  backToChatBtn: {
    marginHorizontal: Spacing.md,
    marginTop: Spacing.lg,
    backgroundColor: Colors.primary,
    borderRadius: Radius.xl,
    paddingVertical: Spacing.md,
    alignItems: 'center',
  },
  backToChatText: {
    fontSize: FontSize.md,
    color: '#FFF',
    fontWeight: '700',
  },
});
