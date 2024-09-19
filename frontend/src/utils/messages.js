const Messages = {
  previous: "上一步",
  next: "下一步",
  submit: "&ensp;發送&ensp;",

  stepTitle: "Step",

  step1Title: "輸入你的官方帳號管理網址",
  step1InputPlaceholder: "Please Input",
  step1HowToTitle: "如何取得官方帳號管理網址？",
  step1HowToHtml: `
  <ol>
    <li>進入<a href="https://manager.line.biz/">官方帳號管理頁面</a>，並登入你的 LINE 帳號</li>
      <img src="/img/fetchURL-step1.png" alt="step1" width="400px">
    <li>點選你要群發訊息的官方帳號</li>
      <img src="/img/fetchURL-step2.png" alt="step2" height="300px">
    <li>點選左上角的「聊天」選項</li>
      <img src="/img/fetchURL-step3.png" alt="step3" width="400px">
    <li>複製網址列的網址</li>
      <img src="/img/fetchURL-step4.png" alt="step4" height="300px">
  </ol>

  `,

  step2Title: "選擇訊息類型",

  messageTypeText: "純文字訊息（包含表情符號）",
  messageTypeDocument: "檔案訊息（包含圖片、影片、文件等等）",
  messageTypeSticker: "貼圖",

  messageTypeNotSupport: "（目前不支援此類型訊息）",

  step3TextTitle: "輸入文字",
  step3TextInputPlaceholder: "Please Input",

  step3DocumentTitle: "上傳文件",
  step3StickerTitle: "選擇貼圖",

  submitComfirmTitle: "確定要發送嗎？",
  submitComfirmComfirm: "確定",
  submitComfirmCancel: "取消",

  submitSuccessMessage: "訊息已成功發送！",
};

export default Messages;