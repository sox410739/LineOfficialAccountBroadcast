<script setup>
import { computed } from "vue";
import { UploadFilled } from "@element-plus/icons-vue";
import StepContent from "./StepContent.vue";
import Messages from "../utils/messages";
import { MessageType } from "../utils/types";
import { genFileId } from "element-plus";
import { ref } from "vue";

const props = defineProps({
  messageType: {
    type: String,
    required: true,
  },
});

const message = defineModel();

// Title
const title = computed(() => {
  switch (props.messageType) {
    case MessageType.TEXT:
      return Messages.step3TextTitle;
    case MessageType.DOCUMENT:
      return Messages.step3DocumentTitle;
    case MessageType.STICKER:
      return Messages.step3StickerTitle;
    default:
      return "";
  }
});

// Document - Upload
const handleRemove = (file) => {
  message.value = "";
};

const handleChange = (file, fileList) => {
  message.value = file.raw;
};

const upload = ref();

const handleExceed = (files, fileList) => {
  upload.value.clearFiles();
  const file = files[0];
  file.uid = genFileId();
  upload.value.handleStart(file);
};
</script>

<template>
  <StepContent :title="title">
    <!-- Text - Input -->
    <el-input
      v-if="messageType === MessageType.TEXT"
      v-model="message"
      :placeholder="Messages.step3TextInputPlaceholder"
      :autosize="{ minRows: 3 }"
      style="width: 100%"
      size="large"
      type="textarea"
    />

    <!-- Document - Upload -->
    <el-upload
      v-else-if="messageType === MessageType.DOCUMENT"
      class="upload-demo"
      drag
      action="#"
      ref="upload"
      :auto-upload="false"
      :limit="1"
      :on-remove="handleRemove"
      :on-change="handleChange"
      :on-exceed="handleExceed"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">Files with a size less than 1GB</div>
      </template>
    </el-upload>
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