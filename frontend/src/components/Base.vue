<script setup>
import axios from "axios";
import { computed, ref } from "vue";
import { ArrowLeft, ArrowRight, Promotion } from "@element-plus/icons-vue";
import Messages from "../utils/messages";
import { MessageType } from "../utils/types";
import Step1 from "./Step1.vue";
import Step2 from "./Step2.vue";
import Step3 from "./Step3.vue";

const totalSteps = 3;
const step = ref(0);

const link = ref("");
const messageType = ref(MessageType.TEXT);
const message = ref("");

const previousMessageType = ref(MessageType.TEXT);
const isSubmitting = ref(false);

// Previous
const previousVisibility = computed(() => {
  return step.value > 0 ? "visible" : "hidden";
});

const previous = () => {
  if (step.value > 0) {
    step.value--;
  }
};

// Next
const nextText = computed(() => {
  return step.value === totalSteps - 1 ? Messages.submit : Messages.next;
});

const nextIcon = computed(() => {
  return step.value === totalSteps - 1 ? Promotion : ArrowRight;
});

const canNext = computed(() => {
  return !isSubmitting.value && validate();
});

const next = () => {
  if (!validate()) {
    return;
  }
  if (step.value < totalSteps - 1) {
    step.value++;
    if (step.value === 2) {
      if (messageType.value !== previousMessageType.value) {
        message.value = "";
      }
      previousMessageType.value = messageType.value;
    }
  } else {
    ElMessageBox.confirm("", Messages.submitComfirmTitle, {
      confirmButtonText: Messages.submitComfirmComfirm,
      cancelButtonText: Messages.submitComfirmCancel,
      distinguishCancelAndClose: true,
    }).then(async () => {
      isSubmitting.value = true;
      await submitGo();
      isSubmitting.value = false;
    });
  }
};

const submitGo = async () => {
  try {
    const response = await submit();
    if (response.data.status === "success") {
      ElMessage.success(Messages.submitSuccessMessage);
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    ElMessage.error(error.message);
  }
};

// Submit
const submit = async () => {
  if (messageType.value === MessageType.TEXT) {
    return await submitText();
  } else if (messageType.value === MessageType.DOCUMENT) {
    return await submitFile();
  }
  throw new Error("This type not support");
};

const submitText = async () => {
  return await axios.post("/api/crawler/message", {
    url: link.value,
    message: message.value,
  });
};

const submitFile = async () => {
  const formData = new FormData();
  formData.append("url", link.value);
  formData.append("file", message.value);
  return await axios.post("/api/crawler/file", formData);
};

// Validate
const validate = () => {
  if (step.value === 0) {
    return validateLink();
  } else if (step.value === 1) {
    return validateMessageType();
  } else if (step.value === 2) {
    return validateMessage();
  }
};

const validateLink = () => {
  const regex = /^https:\/\/chat.line.biz\/U[a-f0-9]{32}\/chat\/U[a-f0-9]{32}$/;
  return regex.test(link.value);
};

const validateMessageType = () => {
  return Object.values(MessageType).includes(messageType.value);
};

const validateMessage = () => {
  return message.value !== "";
};
</script>

<template>
  <div class="content-background">
    <!-- Previous -->
    <div class="previous">
      <el-button
        type="primary"
        class="action-button"
        :style="{ visibility: previousVisibility }"
        @click="previous"
      >
        <el-icon class="el-icon--left">
          <ArrowLeft />
        </el-icon>
        <p>{{ Messages.previous }}</p>
      </el-button>
    </div>

    <!-- Content -->
    <div class="body">
      <div class="stepper-background">
        <el-steps
          class="stepper"
          :active="step"
          align-center
          finish-status="success"
        >
          <el-step
            v-for="num in totalSteps"
            :title="Messages.stepTitle + ' ' + num"
            :key="num"
          />
        </el-steps>
      </div>

      <div class="body">
        <Step1 v-if="step === 0" v-model="link" />
        <Step2 v-if="step === 1" v-model="messageType" />
        <Step3 v-if="step === 2" v-model="message" :messageType="messageType" />
      </div>
    </div>

    <!-- Next -->
    <div class="next">
      <el-button
        type="primary"
        class="action-button"
        @click="next"
        :disabled="!canNext"
      >
        <p v-html="nextText" />
        <el-icon class="el-icon--right">
          <component :is="nextIcon"></component>
        </el-icon>
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.stepper-background {
  background-color: var(--el-color-primary);
  padding: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.stepper {
  width: 100%;
  background-color: white;
  padding: 0.5rem;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.content-background {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  padding: 1rem;
  gap: 0.5rem;
  box-sizing: border-box;
}

.content-background > .previous,
.next {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.content-background > .body {
  border: var(--el-color-primary);
  border-style: solid;
  border-radius: 0.5rem;
  max-width: 100%;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 600px;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
}

.content-background > .body > .body {
  max-width: 100%;
  height: 100%;
  overflow: hidden;
  padding: 1rem;
  min-width: 600px;
  display: flex;
  flex-direction: column;
}
</style>