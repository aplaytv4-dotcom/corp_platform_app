import { ref } from "vue";

export function useAsyncState(initialValue = null) {
  const data = ref(initialValue);
  const loading = ref(false);
  const error = ref("");

  async function run(callback) {
    loading.value = true;
    error.value = "";
    try {
      data.value = await callback();
      return data.value;
    } catch (err) {
      error.value = err?.response?.data?.detail || err?.message || "Unknown error";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    data,
    loading,
    error,
    run,
  };
}
