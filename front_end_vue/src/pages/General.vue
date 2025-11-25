<template>
    <v-card>
      <v-layout>
        <v-navigation-drawer>
          <v-list density="compact" nav>
            <router-link to="/" class="no-underline">
              <v-list-item prepend-icon="mdi-plus" title="Upload files" @click ="selectedItem = 'UploadPage'"></v-list-item>
            </router-link>
            <router-link to="/docs" class="no-underline">
              <v-list-item prepend-icon="mdi-folder" title="Documents" @click ="selectedItem = 'DataTable'"></v-list-item>
            </router-link>
            <router-link to="/tickets" class="no-underline">
              <v-list-item prepend-icon="mdi-account-multiple" title="Tickets" @click ="selectedItem = 'DataTable'"></v-list-item>
            </router-link>
            <router-link to="/Photos" class="no-underline">
              <v-list-item prepend-icon="mdi-image" title="Photos" value="photos"></v-list-item>
            </router-link>
            <router-link to="/rand" class="no-underline">
              <v-list-item prepend-icon="mdi-star" title="Random" value="random"></v-list-item>
            </router-link>
          </v-list>
        </v-navigation-drawer>
  
        <v-main style="height: 100vh; width: 100vw">
            <v-div>
                <component :is="selectedItem" />
            </v-div> 
        </v-main>
      </v-layout>
    </v-card>
</template>

<script>
let selectedItem = "Default"
import DataTable from "../components/DataTable.vue"
import UploadPage from "../components/Upload.vue"
export default {
  name: 'SideBar',
  components: {
    UploadPage, // Correctly register UploadPage as a component
    DataTable
  },
  data() {
    return {
      selectedItem: 'UploadPage', // Default component to show
    };
  },
};
console.log(selectedItem)
</script>

<style>
.no-underline {
  text-decoration: none;
}
</style>