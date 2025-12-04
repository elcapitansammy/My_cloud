<template>
  <v-file-input
    label="File input"
    @change="handleFileSelect" 
    ref="fileInput"
    counter
    multiple
    show-size
  ></v-file-input>
          <v-select style="padding-top: 5%;"
        label="Select Category" v-model="selectedItem" @update:modelValue="selectItem"
        :items="['Documents', 'Tickets','Random', 'Photos']">
        </v-select>
        <v-select style="padding-top: 5%;"
        label="Select User" v-model="selectedUser" @update:modelValue="selectUser"
        :items="['Samuele', 'Daniel', 'Mamma', 'Nicolas', 'Babbo']">
        </v-select>
          <v-btn class="mt-5" @click="uploadFiles" :disabled="disabled">
         Upload Files on {{ currentPath }}
       </v-btn>
</template>

<script>
import { API_BASE_URL, BASE_PATH } from '../config';
import axios from 'axios';
export default {
  data() {
    return {
      selectedFiles: [],
      selectedItem: null,
      selectedUser: null,
      uploading: null,
      basePath: BASE_PATH, // Default upload path
      disabled: true
    }
  },
    computed: {
    // Current path is always Category/User
    currentPath() {
      if (this.selectedItem && this.selectedUser) {
        return `${this.basePath}/${this.selectedItem}/${this.selectedUser}`;
      } else if (this.selectedItem) {
        return `${this.basePath}/${this.selectedItem}`;
      } else if (this.selectedUser) {
        return `${this.basePath}/${this.selectedUser}`;
      } else {
        return this.basePath;
      }
    },
    disabled() {
      // Upload button enabled only if both category and user are selected
      return !(this.selectedItem && this.selectedUser && this.selectedFiles.length > 0);
    }
  },
  methods: {
    selectItem(item) {
      this.selectedItem = item;
      // Reset user if needed
      if (this.selectedUser) this.selectedUser = null;
      console.log('Selected category:', item);
    },
    selectUser(user) {
      this.selectedUser = user;
      console.log('Selected user:', user);
    },
    handleFileSelect(event) {
      this.selectedFiles = Array.from(event.target.files);
    },
    
    async uploadFiles() {
      if (!this.selectedFiles.length) return;
      
      this.uploading = true;
      this.disabled = true;
      
      for (const file of this.selectedFiles) {
        await this.uploadSingleFile(file);
      }
      console.log(`upload successfully`);
      this.uploading = false;
      this.selectedFiles = [];
      this.$refs.fileInput.value = '';
      this.disabled = false;
      alert("All files uploaded successfully!");
    },
    
    async uploadSingleFile(file) {
      const formData = new FormData();
      formData.append('file', file);
  
      try {
        const response = await axios.post(
        `${API_BASE_URL}/upload?destination=${encodeURIComponent(this.currentPath)}/`, 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      console.log('Upload response:', response.data);

      } catch (error) {
        console.error('Upload error:', error);
      }
    }
  }
}
</script>

<style scoped>
</style>