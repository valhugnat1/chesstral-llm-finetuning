<template>
  <div class="chat-container">
    <div v-if="chatStore.isLoading">Loading messages...</div>
    <div v-else-if="chatStore.error">{{ chatStore.error }}</div>
    <div v-else class="messages" ref="messagesContainer">
      <div
        v-for="message in chatStore.getAllMessages"
        :key="message.id"
        :class="[
          'message',
          message.person.id === chatStore.currentUser.id
            ? 'user-message'
            : 'other-message',
        ]"
      >
        <div class="message-header">
          <strong>{{ message.person.name }}</strong>
          <small>{{ formatTime(message.timestamp) }}</small>
        </div>
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from "vue";
import { useChatStore } from "../stores/chatStore";

const chatStore = useChatStore();
const newMessage = ref("");
const messagesContainer = ref(null);

// Fonction pour faire défiler jusqu'au bas du conteneur de messages
const scrollToBottom = () => {
  if (messagesContainer.value) {
    nextTick(() => {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    });
  }
};

onMounted(() => {
  // Load initial messages
  chatStore.fetchMessages().then(() => {
    scrollToBottom();
  });
});

// Observer les changements de messages pour faire défiler automatiquement
watch(
  () => chatStore.getAllMessages.length,
  () => {
    scrollToBottom();
  }
);

function sendMessage() {
  if (newMessage.value.trim()) {
    chatStore.addUserMessage(newMessage.value);
    newMessage.value = "";
    // Simulate response
    setTimeout(() => {
      chatStore.addOtherMessage("user2", "Alice", "Thanks for your message!");
    }, 1000);
  }
}

function formatTime(date) {
  return new Date(date).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 80vh; /* 80% de la hauteur de la fenêtre */
  width: 300px;
  border: #4caf50 solid 1px;
  margin: 0 auto;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
  max-height: 100%;
  width: 300px;
}

.message {
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 8px;
  max-width: 80%;
}

.user-message {
  background-color: #dcf8c6;
  align-self: flex-end;
  margin-left: auto;
}

.other-message {
  background-color: #f1f0f0;
  align-self: flex-start;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 0.8em;
}

.message-content,
strong,
small {
  color: black;
}

.message-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #eee;
}

input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 8px;
}

button {
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
