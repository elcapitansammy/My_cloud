<template>
    <v-container style="height: 100vh; width: 50vw; padding-top: 5%; ">
        <v-container style = "align-items: center; display: flex; width: 10vw; justify-content: center;">
            <svg height="20vh" width="20vw" viewBox="0 0 24 24" id="upload"><path d="M8.71,7.71,11,5.41V15a1,1,0,0,0,2,0V5.41l2.29,2.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42l-4-4a1,1,0,0,0-.33-.21,1,1,0,0,0-.76,0,1,1,0,0,0-.33.21l-4,4A1,1,0,1,0,8.71,7.71ZM21,12a1,1,0,0,0-1,1v6a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V13a1,1,0,0,0-2,0v6a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V13A1,1,0,0,0,21,12Z"></path></svg>
        </v-container>
        <UploadFile></UploadFile>
    </v-container>
  </template>
  
  <script>
  import UploadFile from "./UploadFile.vue"
  export default {
    name: 'UploadPage'
    , components: {UploadFile}
    , methods: {
      async Uploadfile(){
      }
    }
  };
  </script>
  
<style scoped>
  /* Add scoped styles for the component */
.v-layout {
    height: 100%; /* Ensure the layout fills the container */
    width: 100%;
}
  
/* Scoped styles for the component */
.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* Ensure the container fills its parent vertically */
  width: 100%;
}

.svg {
  width: 100%; /* Optionally set width to fill container */
  height: auto; /* Maintain aspect ratio */
}
  </style>
  