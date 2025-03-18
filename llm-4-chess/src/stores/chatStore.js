// stores/chatStore.js
import { defineStore } from "pinia";
import { h } from "vue";

export const useChatStore = defineStore("chat", {
  state: () => ({
    messages: [],
    currentUser: {
      id: "user1",
      name: "Current User",
    },
    isLoading: false,
    error: null,
  }),

  getters: {
    // Get all messages
    getAllMessages: (state) => state.messages,

    // Get messages count
    getMessageCount: (state) => state.messages.length,

    // Get messages grouped by sender
    getMessagesBySender: (state) => {
      const grouped = {};
      state.messages.forEach((message) => {
        if (!grouped[message.person.id]) {
          grouped[message.person.id] = [];
        }
        grouped[message.person.id].push(message);
      });
      return grouped;
    },

    // Get only user messages
    getUserMessages: (state) => {
      return state.messages.filter(
        (message) => message.person.id === state.currentUser.id
      );
    },

    // Get only other people's messages
    getOtherMessages: (state) => {
      return state.messages.filter(
        (message) => message.person.id !== state.currentUser.id
      );
    },
  },

  actions: {
    // Add a new message
    addMessage(personId, personName, content) {
      const newMessage = {
        id: Date.now().toString(),
        person: {
          id: personId,
          name: personName,
        },
        content: content,
        timestamp: new Date(),
      };

      this.messages.push(newMessage);
      return newMessage;
    },

    // Add message from current user
    addUserMessage(content) {
      return this.addMessage(
        this.currentUser.id,
        this.currentUser.name,
        content
      );
    },

    // Add message from another person
    addOtherMessage(personId, personName, content) {
      return this.addMessage(personId, personName, content);
    },

    // Delete a message by ID
    deleteMessage(messageId) {
      const index = this.messages.findIndex(
        (message) => message.id === messageId
      );
      if (index !== -1) {
        this.messages.splice(index, 1);
        return true;
      }
      return false;
    },

    // Update a message by ID
    updateMessage(messageId, newContent) {
      const message = this.messages.find((message) => message.id === messageId);
      if (message) {
        message.content = newContent;
        message.edited = true;
        return true;
      }
      return false;
    },

    // Clear all messages
    clearMessages() {
      this.messages = [];
    },

    // Set current user
    setCurrentUser(userId, userName) {
      this.currentUser = {
        id: userId,
        name: userName,
      };
    },

    // Simulate loading messages from an API
    async fetchMessages() {
      this.isLoading = true;
      this.error = null;

      try {
        // Simulating API call with setTimeout
        await new Promise((resolve) => setTimeout(resolve, 500));

        // Example data
        const sampleMessages = [];

        this.messages = sampleMessages;
      } catch (err) {
        this.error = "Failed to fetch messages";
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
  },
});
