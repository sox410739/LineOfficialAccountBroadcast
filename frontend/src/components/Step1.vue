<script setup>
import { ref } from "vue";
import StepContent from "./StepContent.vue";
import Messages from "../utils/messages";

const link = defineModel();
const dialogVisible = ref(false);
</script>

<template>
  <StepContent :title="Messages.step1Title">
    <!-- Input -->
    <el-input
      v-model="link"
      :placeholder="Messages.step1InputPlaceholder"
      style="width: 100%"
      size="large"
      clearable
    />

    <!-- How To Button -->
    <el-button
      @click="dialogVisible = true"
      type="primary"
      size="small"
      style="width: 100%"
      text
    >
      {{ Messages.step1HowToTitle }}
    </el-button>

    <!-- How To Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="Messages.step1HowToTitle"
      max-width="80%"
      align-center
    >
      <div v-html="Messages.step1HowToHtml" />
    </el-dialog>
  </StepContent>
</template>