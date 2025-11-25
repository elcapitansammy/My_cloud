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
      uploading: false, 
      currentPath: BASE_PATH, // Default upload path
      disabled: true
    }
  },
  methods: {
    selectItem(item) {
      this.selectedItem = item;
      console.log('Selected item:', item);
      this.currentPath = item === 'Documents' ? 'T7 FEB1/Documents' :
                         item === 'Tickets' ? 'T7 FEB1/Tickets' :
                         item === 'Random' ? 'T7 FEB1/Random' :
                         item === 'Photos' ? 'T7 FEB1/Photos' : 'T7 FEB1';
      this.disabled = false;
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