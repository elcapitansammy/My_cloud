<template>
  <v-card
    title="Available Documents"
    flat
  >
    <v-card class = "container">
      <!-- Path Navigation -->
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-folder</v-icon>
        Current Path: {{ currentPath }}
        <v-spacer></v-spacer>
        <v-btn 
          color="primary" 
          size="small" 
          @click="createDirectory(prompt('Enter directory name:'))"
          class="mr-2"
        >
          <v-icon>mdi-folder-plus</v-icon>
          New Folder
        </v-btn>
        <v-btn 
          color="secondary" 
          size="small" 
          @click="fetchFiles()"
          :loading="loading"
        >
          <v-icon>mdi-refresh</v-icon>
          Refresh
        </v-btn>
      </v-card-title>
      
      <!-- Path Input -->
      <v-card-text>
        <v-text-field
          v-model="currentPath"
          label="Path"
          append-icon="mdi-folder-search"
          @click:append="fetchFiles"
          @keyup.enter="fetchFiles"
          hint="Enter path like 'genti' or 'genti/Downloads'"
          persistent-hint
          class="mb-4"
        ></v-text-field>
      </v-card-text>

      <!-- Search Bar -->
      <v-toolbar class="px-2">
        <v-text-field
          v-model="search"
          density="comfortable"
          placeholder="Search files"
          prepend-inner-icon="mdi-magnify"
          style="max-width: 100%;"
          variant="solo"
          clearable
          hide-details
        ></v-text-field>
      </v-toolbar>

      <!-- Scrollable Files Container -->
      <div class="files-container">
        <v-container class="pa-2">
          <!-- Loading State -->
          <v-row v-if="loading" justify="center" class="my-5">
            <v-col cols="auto">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <p class="text-center mt-2">Loading files...</p>
            </v-col>
          </v-row>
          
          <!-- Empty State -->
          <v-row v-else-if="!filteredFiles.length" justify="center" class="my-5">
            <v-col cols="auto" class="text-center">
              <v-icon size="64" color="grey-lighten-1">mdi-folder-open-outline</v-icon>
              <p class="text-h6 mt-2">No files found</p>
              <p class="text-body-2 text-medium-emphasis">This directory is empty or the path doesn't exist</p>
            </v-col>
          </v-row>
          
          <!-- Files Grid -->
          <v-row v-else dense class="files-grid">
            <v-col
              v-for="file in filteredFiles"
              :key="file.name"
              cols="auto"
              md="3"
            >
              <v-card 
                class="pb-3" 
                border 
                flat
                :class="{ 'directory-card': file.isDirectory }"
                @click="file.isDirectory ? navigateToDirectory(file.path) : null"
                :style="{ cursor: file.isDirectory ? 'pointer' : 'default' }"
              >
                <!-- FILE PREVIEW -->
                <div>
                  <!-- Image Preview -->
                  <v-img
                    v-if="file.type === 'Image'"
                    :src="file.url"
                    height="200"
                    cover
                  ></v-img>

                  <!-- PDF Preview -->
                  <iframe
                    v-else-if="file.name.toLowerCase().endsWith('.pdf')"
                    :src="file.url"
                    style="width: 100%; height: 200px; border: none;"
                  ></iframe>

                  <!-- Default Icon -->
                  <v-img
                    v-else
                    :src="file.img"
                    height="200"
                    cover
                  ></v-img>
                </div>

                <v-list-item :subtitle="file.type" class="mb-2">
                  <template v-slot:title>
                    <strong class="text-h9 mb-2">
                      <v-icon v-if="file.isDirectory" class="mr-1">mdi-folder</v-icon>
                      {{ file.name }}
                    </strong>
                  </template>
                </v-list-item>

                <div class="d-flex justify-space-between px-4">
                  <div class="d-flex align-center text-caption text-medium-emphasis me-1">
                    <v-icon :icon="file.isDirectory ? 'mdi-folder-outline' : 'mdi-file-outline'" start></v-icon>

                    <div class="text-truncate">{{ file.size }}</div>
                  </div>

                  <div class="d-flex gap-2" v-if="!file.isDirectory">
                    <v-btn
                      class="text-none"
                      size="small"
                      text="Download"
                      color="primary"
                      variant="outlined"
                      :href="file.url"
                      target="_blank"
                    >
                      <v-icon>mdi-download</v-icon>
                    </v-btn>
                    
                    <v-btn
                      size="small"
                      color="error"
                      variant="outlined"
                      @click="deleteFile(file.path)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </div>
                  
                  <div class="d-flex gap-2" v-else>
                    <v-btn
                      size="small"
                      color="primary"
                      variant="outlined"
                      @click.stop="navigateToDirectory(file.path)"
                    >
                      <v-icon>mdi-folder-open</v-icon>
                      Open
                    </v-btn>
                  </div>
                </div>
              </v-card>
            </v-col>
          </v-row>
          
          <!-- Spacer at the end -->
          <div class="bottom-spacer"></div>
        </v-container>
      </div>
    </v-card>
  </v-card>
</template>

<style>

.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.files-container {
  flex-grow: 1;
  height: 75vh;
  overflow-y: auto;
  padding-bottom: 20px;
}

/* Custom scrollbar for better UX */
.files-container::-webkit-scrollbar {
  width: 8px;
}

.files-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.files-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.files-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Directory hover effect */
.directory-card:hover {
  background-color: #f5f5f5;
  transform: translateY(-2px);
  transition: all 0.2s ease;
}

/* Bottom spacer */
.bottom-spacer {
  height: 100px;
  width: 100%;
}
</style>

<script>
import axios from 'axios';
import { API_BASE_URL, BASE_PATH } from '../config';
  
  export default {
    name: "DataTable", 
    data() {
      return {
        search: '',
        files: [],
        currentPath: BASE_PATH, // Default path
        apiBaseUrl: API_BASE_URL, // Direct FastAPI call
        loading: false,
        selectedFile: null,
      };
    },
    created() {
      this.currentPath = this.filePath; 
      this.fetchFiles();
    },props: {
      filePath: {
        type: String,
        required: true
      }
    },
    computed: {
      filteredFiles() {
        let files = this.files;
        
        // Filter by search term if provided
        if (this.search) {
          files = files.filter(file => 
            file.name.toLowerCase().includes(this.search.toLowerCase())
          );
        }
        
        // Sort: directories first, then files alphabetically
        return files.sort((a, b) => {
          // Directories come first
          if (a.isDirectory && !b.isDirectory) return -1;
          if (!a.isDirectory && b.isDirectory) return 1;
          
          // Within same type, sort alphabetically
          return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
        });
      }
    },
    methods: {
      async fetchFiles() {
        console.log(this.filePath); 
        this.loading = true;
        try {
          const url = this.currentPath 
            ? `${this.apiBaseUrl}/list?path=${encodeURIComponent(this.currentPath)}`
            : `${this.apiBaseUrl}/list`;
            
          const response = await axios.get(url);
          
          //console.log('Raw API response:', response.data);
          
          // Handle different response formats from your FastAPI
          let filesData = response.data;
          
          // If response.data is an object with a files property
          if (filesData && typeof filesData === 'object' && filesData.files) {
            filesData = filesData.files;
          }
          
          // If response.data is not an array, make it an array
          if (!Array.isArray(filesData)) {
            console.warn('API response is not an array:', filesData);
            filesData = [];
          }
          
          this.files = filesData.map(item => {
            const name = item.name || item.filename || item;
            const isDirectory = item.is_directory || item.isDirectory || this.isDirectoryByName(name);
            
            return {
              name: name,
              path: item.path || `${this.currentPath}/${name}`,
              size: isDirectory ? 'Directory' : (item.size || 'Unknown'),
              type: this.getFileType(name, isDirectory),
              isDirectory: isDirectory,
              url: item.url || `${this.apiBaseUrl}/download?path=${encodeURIComponent(item.path || `${this.currentPath}/${name}`)}`,
              previewType: this.getPreviewType(name),  // PREVIEW TYPE ADDED
              img: this.getFileIcon(name, isDirectory)
            };
          });
          
          console.log('Processed files:', this.files);
        } catch (error) {
          console.error('Error fetching files:', error);
          this.files = [];
        } finally {
          this.loading = false;
        }
      },
      
      async deleteFile(filePath) {
        if (!confirm(`Are you sure you want to delete ${filePath}?`)) return;
        
        try {
          await axios.post(`${this.apiBaseUrl}/delete?path=${encodeURIComponent(filePath)}`);
          this.fetchFiles(); // Refresh the list
          console.log('File deleted successfully');
        } catch (error) {
          console.error('Error deleting file:', error);
          alert('Failed to delete file');
        }
      },
      
      async createDirectory(dirName) {
        if (!dirName) return;
        
        try {
          const newDirPath = `${this.currentPath}/${dirName}`;
          await axios.post(`${this.apiBaseUrl}/create-directory?path=${encodeURIComponent(newDirPath)}`);
          this.fetchFiles(); // Refresh the list
          console.log('Directory created successfully');
        } catch (error) {
          console.error('Error creating directory:', error);
          alert('Failed to create directory');
        }
      },
      
      changePath(newPath) {
        this.currentPath = newPath;
        this.fetchFiles();
      },
      getPreviewType(name) {
        if (!name) return null;
        const ext = name.toLowerCase();

        if (ext.match(/\.(jpg|jpeg|png|gif|bmp|webp|svg)$/)) return 'image';
        if (ext.match(/\.pdf$/)) return 'pdf';

        return null;
      },
      
      navigateToDirectory(dirPath) {
        this.currentPath = dirPath;
        this.fetchFiles();
      },
      
      isDirectoryByName(name) {
        // If no extension and doesn't look like a file, it's probably a directory
        return name && !name.includes('.') && !name.match(/\.(.*)/);
      },
      
      getFileType(filename, isDirectory = false) {
        if (!filename) return 'Unknown';
        
        if (isDirectory) {
          return 'Directory';
        }
        
        const ext = filename.split('.').pop()?.toLowerCase();
        const typeMap = {
          'pdf': 'PDF Document',
          'doc': 'Word Document', 'docx': 'Word Document',
          'xls': 'Excel Spreadsheet', 'xlsx': 'Excel Spreadsheet',
          'ppt': 'PowerPoint', 'pptx': 'PowerPoint',
          'jpg': 'Image', 'jpeg': 'Image', 'png': 'Image', 'gif': 'Image', 'heic': 'Image',
          'mp4': 'Video', 'avi': 'Video', 'mov': 'Video',
          'mp3': 'Audio', 'wav': 'Audio',
          'zip': 'Archive', 'rar': 'Archive', '7z': 'Archive',
          'txt': 'Text File',
        };
        return typeMap[ext] || 'File';
      },
      
      getFileIcon(filename, isDirectory = false) {
        if (!filename) return '';        
        if (isDirectory) {
          return '/icons/folder.png'; // You can replace with actual folder icon
        }
        
        const ext = filename.split('.').pop()?.toLowerCase();
        // Return placeholder or actual icon URLs based on file type
        const iconMap = {
          'pdf': '/icons/pdf.png',
          'doc': '/icons/word.png', 'docx': '/icons/word.png',
          'xls': '/icons/excel.png', 'xlsx': '/icons/excel.png',
          'jpg': '/icons/image.png', 'jpeg': '/icons/image.png', 'png': '/icons/image.png', 'heic': '/icons/image.png',
          'mp4': '/icons/video.png', 'mov': '/icons/video.png',
          'zip': '/icons/archive.png',
        };
        return iconMap[ext] || '/icons/file.png';
      },
    },
  };
  </script>
