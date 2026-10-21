# 🔴🔴 OBSOLETE — DO NOT USE 🔴🔴

> This repository is superseded and should not be used for new builds or
> releases. The maintained canonical source is
> **[axelites/dify-plugin-storage](https://github.com/axelites/dify-plugin-storage)**.
> Version 0.0.5 and all future fixes are maintained there.

## storage

**Author:** hjlarry  
**Version:** 0.0.1  
**Type:** extension  
**Repo:** :[https://github.com/hjlarry/dify-plugin-storage](https://github.com/hjlarry/dify-plugin-storage)

### Description

This plugin is a key-value storage tool allow you save and get data across different apps.


### Example Usage

#### 1. Persistent Token Management Across Applications

Similar to Redis or the conversation variables in Dify, you can use tools that allow data persistence across different applications. For instance, when requesting an API service in your Dify workflow, you might first need to obtain a temporary token. You can utilize the set_string tool to save this token.

When users execute your workflow, they can retrieve the token using the get_string tool, minimizing the need to repeatedly request a new temporary token. This capability ensures that data can be shared seamlessly across applications and stored for long-term use.


#### 2. Secure File Sharing from Dify App

Due to security, direct access to a file's URL in Dify is restricted; the preview file URL is valid for only 300 seconds. To address this, you can use the save_file tool to store the file persistently and share it via a generated endpoint.

The shared url will look like this: `https://daemon-plugin.dify.dev/rbmcB5EZRdDAlOqTt3H9ApgWcjzfD9Jg/file?key=your-file-key`.

To enhance security, you can include an api_key in the endpoint, resulting in a URL like: `https://daemon-plugin.dify.dev/rbmcB5EZRdDAlOqTt3H9ApgWcjzfD9Jg/file?key=your-file-key&api_key=your-api-key`. If you need to restrict access to the file, simply change the api_key, rendering the original URL inaccessible.
