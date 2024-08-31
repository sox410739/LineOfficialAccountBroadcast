<script setup>
import StepContent from "./StepContent.vue";
import Messages from "../utils/messages";
import { MessageType, MessageTypeInfo } from "../utils/types";

const messageType = defineModel();
</script>

<template>
  <StepContent :title="Messages.step2Title">
    <!-- Radio Group -->
    <el-radio-group
      v-model="messageType"
      size="large"
      class="radio-group"
    >
      <el-radio
        v-for="type in MessageType"
        :key="type"
        :value="type"
        :disabled="MessageTypeInfo[type].disabled"
        size="large"
        border
      >
        {{
          MessageTypeInfo[type].name +
          (MessageTypeInfo[type].disabled ? Messages.messageTypeNotSupport : "")
        }}
      </el-radio>
    </el-radio-group>
  </StepContent>
</template>

<style scoped>
.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-start;
}
</style>