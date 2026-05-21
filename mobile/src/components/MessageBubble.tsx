/**
 * MessageBubble — renders a single chat message with distinct styles
 * for user vs bot messages.
 */
import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { Colors, Spacing, Radius, FontSize } from '../theme/colors';

export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface Props {
  message: Message;
  isLatest: boolean;
}

export default function MessageBubble({ message, isLatest }: Props) {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(20)).current;

  useEffect(() => {
    if (isLatest) {
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 350,
          useNativeDriver: true,
        }),
        Animated.spring(slideAnim, {
          toValue: 0,
          tension: 80,
          friction: 12,
          useNativeDriver: true,
        }),
      ]).start();
    } else {
      fadeAnim.setValue(1);
      slideAnim.setValue(0);
    }
  }, [isLatest]);

  const isUser = message.sender === 'user';
  const timeStr = message.timestamp.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <Animated.View
      style={[
        styles.container,
        isUser ? styles.userContainer : styles.botContainer,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      {!isUser && (
        <View style={styles.avatarContainer}>
          <Text style={styles.avatar}>🛠️</Text>
        </View>
      )}
      <View
        style={[
          styles.bubble,
          isUser ? styles.userBubble : styles.botBubble,
        ]}
      >
        <Text
          style={[
            styles.text,
            isUser ? styles.userText : styles.botText,
          ]}
          selectable
        >
          {message.text}
        </Text>
        <Text
          style={[
            styles.time,
            isUser ? styles.userTime : styles.botTime,
          ]}
        >
          {timeStr}
        </Text>
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginVertical: Spacing.xs,
    marginHorizontal: Spacing.md,
    alignItems: 'flex-end',
  },
  userContainer: {
    justifyContent: 'flex-end',
  },
  botContainer: {
    justifyContent: 'flex-start',
  },
  avatarContainer: {
    width: 32,
    height: 32,
    borderRadius: Radius.full,
    backgroundColor: Colors.primaryGlow,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: Spacing.sm,
    marginBottom: 2,
  },
  avatar: {
    fontSize: 16,
  },
  bubble: {
    maxWidth: '78%',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm + 2,
    borderRadius: Radius.xl,
  },
  userBubble: {
    backgroundColor: Colors.userBubble,
    borderBottomRightRadius: Radius.sm,
    marginLeft: 'auto',
  },
  botBubble: {
    backgroundColor: Colors.botBubble,
    borderBottomLeftRadius: Radius.sm,
    borderWidth: 1,
    borderColor: Colors.borderLight,
  },
  text: {
    fontSize: FontSize.md,
    lineHeight: 22,
  },
  userText: {
    color: Colors.userBubbleText,
  },
  botText: {
    color: Colors.botBubbleText,
  },
  time: {
    fontSize: FontSize.xs,
    marginTop: 4,
    alignSelf: 'flex-end',
  },
  userTime: {
    color: 'rgba(255,255,255,0.6)',
  },
  botTime: {
    color: Colors.textMuted,
  },
});
