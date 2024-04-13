<script setup>
import { defineModel } from 'vue';

const model = defineModel();
</script>

<template>
<div class="toggler-wrapper" @click="model = !model">
    <slot name="left" />
    <div class="toggler">
        <div class="toggler-circle" :class="{active: model}" />
    </div>
    <slot name="right" />
</div>
</template>

<style scoped>
.toggler-wrapper {
    display: flex;
    gap: 10px;
    cursor: pointer;
    align-items: center;
}

.toggler {
    position: relative;
    width: 40px;
    height: 20px;
    border-radius: 25px;
    background-color: var(--color-background-mute);
}

.toggler-circle {
    background: hsla(160, 100%, 37%, 1);
    height: 14px;
    width: 14px;
    border-radius: 25px;
    position: absolute;
    left: 3px;
    top: 3px;
    transition: left 0.2s;
}

.toggler-circle.active {
    left: calc(100% - 14px - 3px);
}
</style>