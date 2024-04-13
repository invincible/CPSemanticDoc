<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useDropzone } from "vue3-dropzone";
import VueSelect from "vue-select";
import 'vue-select/dist/vue-select.css';

import BaseToggler from "@/components/BaseToggler.vue";
import IconHTML from "@/components/icons/IconHTML.vue";
import IconPDF from "@/components/icons/IconPDF.vue";
import IconWord from "@/components/icons/IconWord.vue";
import IconTxt from "@/components/icons/IconTxt.vue";
import IconCross from "@/components/icons/IconCross.vue";
import IconZip from "@/components/icons/IconZip.vue";
import BackIcon from "@/components/icons/BackIcon.vue";

const classType = ref(null)

const inputFile = ref(null);

const isText = ref(false);
const documentText = ref(null);
const documentFile = ref(null);
const selectedFiles = ref([]);

const types = ref(["Доверенность", "Договор", "Акт", "Заявление", "Приказ", "Счет", "Приложение", "Соглашение", "Договор оферты", "Устав", "Решение"]);

const url = "https://hui.com/api/huemoe";
const saveFiles = (files) => {
    const formData = new FormData();
    for (var x = 0; x < files.length; x++) {
        formData.append("files[]", files[x]);
    }

    axios
        .post(url, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then((response) => {
            console.info(response.data);
        })
        .catch((err) => {
            console.error(err);
        });
};

function onDrop(acceptFiles, rejectReasons) {
    selectedFiles.value = acceptFiles;
    console.log(rejectReasons);
}

const { getRootProps, getInputProps } = useDropzone({ onDrop });

const getFileType = function (filename) {
    return filename.split('.').at(-1);
}

const isWordFile = function (filename) {
    const types = ["doc", "docx", "rtf", "docm", "dotm", "dotx"];

    return types.includes(getFileType(filename));
}

const isPdfFile = function (filename) {
    return getFileType(filename) === "pdf";
}

const isTextFile = function (filename) {
    return getFileType(filename) === "txt";
}

const isHtmlFile = function (filename) {
    return getFileType(filename) === "html";
}

const isZipFile = function (filename) {
    const types = ["7z", "zip", "rar", "tar", "gz", "bz2", "xz"];

    return types.includes(getFileType(filename));
}

const removeFile = function (filename) {
    selectedFiles.value = selectedFiles.value.filter((file) => file.name !== filename);
}

onMounted(() => {
   axios
        .get('http://51.250.8.113/types')
        .then((response) => {
            console.info(response.data);
            types.value = response.data;
        })
        .catch((err) => {
            console.error(err);
        });
});

const fetchOptions = function (options, search) {
    if (!search || !search.trim()) return options;

    const filtered = options.filter((type) => type.includes(search));

    if (filtered.length === 0) {
        return [`Добавить класс «${search}»`];
    }

    return filtered;
}
</script>

<template>
    <div class="add-files">
        <div class="header">
            <BackIcon class="back" @click="$router.go(-1)"/>
            <h2>Добавление файлов</h2>
            <div></div>
        </div>
        <div style="width: 100%">
            <span>Выберите класс файла</span>
            <vue-select class="select" :options="types" :filter="fetchOptions" />
        </div>
        <BaseToggler v-model="isText">
            <template #left> Выбрать файл </template>
            <template #right> Вставить текст </template>
        </BaseToggler>
        <template v-if="isText">
            <textarea class="textarea" placeholder="Введите текст..." v-model="documentText" />
        </template>
        <template v-else>
            <div class="dropzone" :class="{ 'files': selectedFiles.length > 0 }" v-bind="getRootProps()">
                <input v-bind="getInputProps()" />
                <p v-if="isDragActive">Перетащите файлы сюда...</p>
                <p v-else>Вы можете перетащить сюда файлы или нажать для выбора файлов</p>
                <div v-if="selectedFiles.length > 0" class="selected-files" @click.stop="">
                    <div v-for="(file, index) in selectedFiles" :key="index" class="selected-file">
                        <div class="delete-file" @click="removeFile(file.name)">
                            <IconCross />
                        </div>
                        <div v-if="isWordFile(file.name)"> <IconWord /> </div>
                        <div v-else-if="isPdfFile(file.name)"> <IconPDF /> </div>
                        <div v-else-if="isTextFile(file.name)"> <IconTxt /> </div>
                        <div v-else-if="isHtmlFile(file.name)"> <IconHTML /> </div>
                        <div v-else-if="isZipFile(file.name)"> <IconZip /> </div>
                        <div v-else> Неподдерживаемый тип </div>
                        {{ file.name }}
                    </div>
                </div>
            </div>
        </template>

        <button class="input-file">Отправить</button>

        <input ref="inputFile" id="inputFile" type="file" style="display: none" />
    </div>
</template>

<style scoped>

.add-files {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 25px;
    max-width: 600px;
    margin: 0 auto;
}

.header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.back {
    font-size: 18px;
    cursor: pointer;
}

.delete-file {
    position: absolute;
    right: 10px;
    top: 10px;
    cursor: pointer;
    width: 17px;
    height: 17px;
    background-color: #ff3333;
    color: var(--vt-c-white);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 666px;
    opacity: 0.0;
    transition: all 0.3s;
}

.selected-file {
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 7px;
    border: 1px solid var(--vt-c-divider-light-1);
    gap: 8px;
    font-size: 12px;
    padding: 10px;
    position: relative;
}

.selected-file:hover .delete-file {
    opacity: 0.8;
}

.selected-files {
    margin-top: 20px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
    gap: 10px;
}

input {
    width: 100%;
    background-color: var(--vt-c-black-soft);
    border: 1px solid var(--vt-c-black-mute);
    color: var(--vt-c-text-dark-1);
    padding: 10px;
}

.textarea {
    width: 100%;
    resize: vertical;
    background-color: var(--vt-c-black-soft);
    border-color: var(--vt-c-black-mute);
    outline: none !important;
    min-height: 300px;
    color: var(--vt-c-text-dark-1);
    padding: 10px;
}

.input-file {
    background: hsla(160, 100%, 37%, 1);
    display: inline-block;
    padding: 10px 20px;
    cursor: pointer;
    color: var(--vt-c-text-dark-1);
    border-radius: 7px;
    align-self: center;
    border: none;
    font-size: 16px;
}

@media (max-width: 1000px) {
    .textarea {
        min-height: 200px;
    }
}

.container {
  display: flex;
  flex-direction: column;
  font-family: sans-serif;
}

.container > p {
  font-size: 1rem;
}

.container > em {
  font-size: .8rem;
}

.dropzone {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border-width: 2px;
    border-radius: 2px;
    border-style: dashed;
    background-color: var(--vt-c-black-soft);
    border-color: var(--vt-c-black-mute);
    color: #bdbdbd;
    outline: none;
    transition: border .24s ease-in-out;
    min-height: 300px;
    width: 100%;
}

.dropzone:focus {
    border-color: hsla(160, 100%, 37%, 1);
}

.dropzone.disabled {
  opacity: 0.6;
}

.selected-file svg {
    width: 40px !important;
    height: auto !important;
}

.delete-file svg {
    width: 11px !important;
    height: auto !important;
    position: relative;
    right: 0;
    bottom: 0;
}

.select {
    width: 100%;
    background-color: var(--vt-c-black-soft);
    border-color: var(--vt-c-black-mute);
    color: #bdbdbd;
}

:global(.vs__dropdown-menu) {
    background-color: var(--vt-c-black-mute) !important;
}

:global(.vs__dropdown-option--highlight) {
    background-color: hsla(160, 100%, 37%, 1);
}
</style>