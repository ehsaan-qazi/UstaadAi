/**
 * UstaadJi — AI Service Orchestrator Mobile App
 *
 * Root component with React Navigation stack:
 *   Chat (home) → Booking (confirmation)
 */
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import ChatScreen from './src/screens/ChatScreen';
import BookingScreen from './src/screens/BookingScreen';

export type RootStackParamList = {
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

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Stack.Navigator
        initialRouteName="Chat"
        screenOptions={{
          headerShown: false,
          animation: 'slide_from_right',
          contentStyle: { backgroundColor: '#0A0E1A' },
        }}
      >
        <Stack.Screen name="Chat" component={ChatScreen} />
        <Stack.Screen name="Booking" component={BookingScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
