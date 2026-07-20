   import { getCurrentWindow } from '@tauri-apps/api/window';

const appWindow = getCurrentWindow();

const minimizeButton = document.querySelector(".windowControlButton.minimize") as HTMLButtonElement;
const fullscreenButton = document.querySelector(".windowControlButton.fullscreen") as HTMLButtonElement;
const closeButton = document.querySelector(".windowControlButton.close") as HTMLButtonElement;

minimizeButton.addEventListener("click", () => {
    appWindow.minimize();
})

fullscreenButton.addEventListener("click", () => {
    appWindow.toggleMaximize();
})

closeButton.addEventListener("click", () => {
    appWindow.close();
})