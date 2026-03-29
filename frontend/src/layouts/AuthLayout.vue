<template>
  <div class="auth-layout">
    <div class="auth-card page-card">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
}
.auth-card {
  width: min(460px, 100%);
  padding: 28px;
}
</style>
