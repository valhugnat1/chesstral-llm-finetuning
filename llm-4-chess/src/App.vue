<script setup>
import CustomBoard from "./components/CustomBoard.vue";
import Chat from "./components/Chat.vue";
import "vue3-chessboard/style.css";
</script>

<template>
  <header>
    <!-- <img
      alt="Vue logo"
      class="logo"
      src="./assets/logo.svg"
      width="125"
      height="125"
    /> -->
  </header>

  <main>
    <div class="wrapper">
      <CustomBoard />
      <div class="chat-container">
        <Chat />
      </div>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  .wrapper {
    display: flex; /* Enable Flex container */
    justify-content: space-between;
    gap: 5%;
  }

  .chat-container {
    display: flex;
    justify-content: center;
    align-items: center;

    /* Add any additional styling for the chat container here */
  }
}
</style>
