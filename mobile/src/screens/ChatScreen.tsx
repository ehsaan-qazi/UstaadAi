/**
 * ChatScreen — Main conversational interface for UstaadJi.
 *
 * Features:
 * - Full chat UI with user/bot message bubbles
 * - Session persistence across messages
 * - Typing indicator during pipeline processing
 * - Quick-action suggestion chips
 * - Header with status indicator
 */
import React, { useState, useRef, useCallback } from 'react';
import {
  View,
  Text,
  TextInput,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  StatusBar,
  SafeAreaView,
  Alert,
} from 'react-native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Colors, Spacing, Radius, FontSize } from '../theme/colors';
import MessageBubble, { Message } from '../components/MessageBubble';
import TypingIndicator from '../components/TypingIndicator';
import { sendMessage } from '../api/client';

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
  navigation: NativeStackNavigationProp<RootStackParamList, 'Chat'>;
}

const USER_ID = 'mobile_user_1';

const SUGGESTIONS = [
  '🔧 Mera AC nahi chal raha',
  '💧 Pipe leak ho raha hai',
  '⚡ Bijli ka switch kharab hai',
  '🪚 Darwaza theek karna hai',
];

export default function ChatScreen({ navigation }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      text: 'Assalam-o-Alaikum! 👋\n\nMain hoon UstaadJi — aapka AI service helper.\n\nBatayein, kya masla hai? AC, plumbing, electric, ya carpentry — jو بھی zaroorat ho, bata dein! 🛠️',
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const flatListRef = useRef<FlatList>(null);

  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      flatListRef.current?.scrollToEnd({ animated: true });
    }, 100);
  }, []);

  const handleSend = useCallback(
    async (text?: string) => {
      const msgText = (text ?? inputText).trim();
      if (!msgText || isLoading) return;

      // Add user message
      const userMsg: Message = {
        id: Date.now().toString(),
        text: msgText,
        sender: 'user',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setInputText('');
      setIsLoading(true);
      scrollToBottom();

      try {
        const res = await sendMessage({
          message: msgText,
          user_id: USER_ID,
          session_id: sessionId,
        });

        // Persist session
        if (res.session_id) {
          setSessionId(res.session_id);
        }

        const botMsg: Message = {
          id: (Date.now() + 1).toString(),
          text: res.response,
          sender: 'bot',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, botMsg]);
      } catch (err: any) {
        console.error('[Chat] API error:', err);
        const errorMsg: Message = {
          id: (Date.now() + 1).toString(),
          text: '⚠️ Backend se connect nahi ho pa raha. Please check karo ke server chal raha hai (port 8000).',
          sender: 'bot',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
        scrollToBottom();
      }
    },
    [inputText, isLoading, sessionId, scrollToBottom]
  );

  const handleNewChat = () => {
    Alert.alert(
      'Naya Chat',
      'Kya aap naya conversation shuru karna chahte hain?',
      [
        { text: 'Nahi', style: 'cancel' },
        {
          text: 'Haan',
          onPress: () => {
            setMessages([
              {
                id: 'welcome-' + Date.now(),
                text: 'Assalam-o-Alaikum! 👋\n\nNaya chat shuru! Batayein kya masla hai? 🛠️',
                sender: 'bot',
                timestamp: new Date(),
              },
            ]);
            setSessionId(null);
          },
        },
      ]
    );
  };

  const renderItem = useCallback(
    ({ item, index }: { item: Message; index: number }) => (
      <MessageBubble
        message={item}
        isLatest={index === messages.length - 1}
      />
    ),
    [messages.length]
  );

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar barStyle="light-content" backgroundColor={Colors.background} />

      {/* ── Header ───────────────────────────────────────────────── */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={styles.logoBg}>
            <Text style={styles.logoEmoji}>🛠️</Text>
          </View>
          <View>
            <Text style={styles.headerTitle}>UstaadJi</Text>
            <View style={styles.statusRow}>
              <View
                style={[
                  styles.statusDot,
                  { backgroundColor: isLoading ? Colors.warning : Colors.success },
                ]}
              />
              <Text style={styles.statusLabel}>
                {isLoading ? 'Soch raha hai...' : 'Online'}
              </Text>
            </View>
          </View>
        </View>
        <TouchableOpacity onPress={handleNewChat} style={styles.newChatBtn}>
          <Text style={styles.newChatIcon}>＋</Text>
        </TouchableOpacity>
      </View>

      {/* ── Messages ─────────────────────────────────────────────── */}
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={0}
      >
        <FlatList
          ref={flatListRef}
          data={messages}
          renderItem={renderItem}
          keyExtractor={(item) => item.id}
          style={styles.messageList}
          contentContainerStyle={styles.messageContent}
          showsVerticalScrollIndicator={false}
          ListFooterComponent={isLoading ? <TypingIndicator /> : null}
          onContentSizeChange={scrollToBottom}
        />

        {/* ── Suggestion Chips (only when empty convo) ───────────── */}
        {messages.length <= 1 && !isLoading && (
          <View style={styles.suggestionsContainer}>
            <Text style={styles.suggestionsTitle}>Try these:</Text>
            <View style={styles.suggestionsRow}>
              {SUGGESTIONS.map((s, i) => (
                <TouchableOpacity
                  key={i}
                  style={styles.chip}
                  onPress={() => handleSend(s)}
                  activeOpacity={0.7}
                >
                  <Text style={styles.chipText}>{s}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
        )}

        {/* ── Input Bar ──────────────────────────────────────────── */}
        <View style={styles.inputBar}>
          <TextInput
            style={styles.input}
            placeholder="Apna masla batayein..."
            placeholderTextColor={Colors.textMuted}
            value={inputText}
            onChangeText={setInputText}
            onSubmitEditing={() => handleSend()}
            multiline
            maxLength={2000}
            returnKeyType="send"
            editable={!isLoading}
          />
          <TouchableOpacity
            style={[
              styles.sendBtn,
              (!inputText.trim() || isLoading) && styles.sendBtnDisabled,
            ]}
            onPress={() => handleSend()}
            disabled={!inputText.trim() || isLoading}
            activeOpacity={0.7}
          >
            <Text style={styles.sendIcon}>➤</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  flex: {
    flex: 1,
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
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoBg: {
    width: 42,
    height: 42,
    borderRadius: Radius.full,
    backgroundColor: Colors.primaryGlow,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: Spacing.sm + 2,
  },
  logoEmoji: {
    fontSize: 22,
  },
  headerTitle: {
    fontSize: FontSize.lg,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 2,
  },
  statusDot: {
    width: 7,
    height: 7,
    borderRadius: 4,
    marginRight: 5,
  },
  statusLabel: {
    fontSize: FontSize.xs,
    color: Colors.textMuted,
  },
  newChatBtn: {
    width: 36,
    height: 36,
    borderRadius: Radius.full,
    backgroundColor: Colors.surfaceLight,
    alignItems: 'center',
    justifyContent: 'center',
  },
  newChatIcon: {
    fontSize: 20,
    color: Colors.textSecondary,
    fontWeight: '300',
  },

  // Messages
  messageList: {
    flex: 1,
  },
  messageContent: {
    paddingTop: Spacing.md,
    paddingBottom: Spacing.sm,
  },

  // Suggestions
  suggestionsContainer: {
    paddingHorizontal: Spacing.md,
    paddingBottom: Spacing.sm,
  },
  suggestionsTitle: {
    fontSize: FontSize.xs,
    color: Colors.textMuted,
    marginBottom: Spacing.sm,
  },
  suggestionsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: Spacing.sm,
  },
  chip: {
    backgroundColor: Colors.surfaceLight,
    borderRadius: Radius.full,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    borderWidth: 1,
    borderColor: Colors.borderLight,
  },
  chipText: {
    fontSize: FontSize.sm,
    color: Colors.textSecondary,
  },

  // Input bar
  inputBar: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    backgroundColor: Colors.surface,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  input: {
    flex: 1,
    minHeight: 42,
    maxHeight: 100,
    backgroundColor: Colors.surfaceLight,
    borderRadius: Radius.xl,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm + 2,
    fontSize: FontSize.md,
    color: Colors.textPrimary,
    borderWidth: 1,
    borderColor: Colors.borderLight,
  },
  sendBtn: {
    width: 42,
    height: 42,
    borderRadius: Radius.full,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: Spacing.sm,
  },
  sendBtnDisabled: {
    backgroundColor: Colors.surfaceLight,
  },
  sendIcon: {
    fontSize: 18,
    color: '#FFF',
  },
});
