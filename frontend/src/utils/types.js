import Messages from "./messages";

const MessageType = {
  TEXT: "text",
  DOCUMENT: "document",
  STICKER: "sticker",
};

const MessageTypeInfo = {
  [MessageType.TEXT]: {
    name: Messages.messageTypeText,
    disabled: false,
  },
  [MessageType.DOCUMENT]: {
    name: Messages.messageTypeDocument,
    disabled: false,
  },
  [MessageType.STICKER]: {
    name: Messages.messageTypeSticker,
    disabled: true,
  },
};

export { MessageType, MessageTypeInfo };