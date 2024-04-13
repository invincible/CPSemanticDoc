<script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import SearchIcon from './icons/IconSearch.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
import HelloWorld from './HelloWorld.vue'
</script>

<template>
  <header class="hello">
    <div class="xdd">

      <img src="/logo.png" class="logo" width="200" alt="Tanker" />
      <div class="wrapper">
        <HelloWorld />
      </div>
    </div>
    <div class="items">

      <WelcomeItem>
        <template #icon>
          <div>
          </div>
          <ToolingIcon />
        </template>
        <template #heading> О нашем решении</template>

        Наш продукт решает проблему классификации множества документов. Ведь сейчас поток документов стал объемным и данную задачу невозможно решить без применения технологий.
      </WelcomeItem>
      <WelcomeItem>
        <template #icon>
          <DocumentationIcon />
        </template>
        <template #heading><RouterLink to="/add-files">Добавить документы</RouterLink></template>
        Пополните коллекцию документов, это поможет улучшить точность классификации.
      </WelcomeItem>

      <WelcomeItem>
        <template #icon>
          <CommunityIcon />
        </template>
        <template #heading><RouterLink to="/check-files">Определить класс</RouterLink></template>

        Загрузите файлы и определите класс документа.
      </WelcomeItem>

      <WelcomeItem>
        <template #icon>
          <SearchIcon />
        </template>
        <template #heading><RouterLink to="/add-files">Поиск</RouterLink></template>

        Найдите нужный документ по ключевым словам.
      </WelcomeItem>
    </div>
  </header>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.xdd {
  display: flex;
  align-items: center;
  flex-direction: column;
  margin: 0 10% 0 0;
  text-align: center;
}

.logo {
  display: block;
  flex-shrink: 0;
  margin: 0 auto 0.5rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.items {
  padding-bottom: 30px;
}

@media (max-width: 1024px) {
  .xdd {
    flex-direction: column;
    margin: 0 0 50px 0;
  }

  .logo {
    display: block;
    flex-shrink: 0;
    margin: 0 0 0.5rem 0;
  }
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 0.5rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
