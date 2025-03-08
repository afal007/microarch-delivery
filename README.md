# microarch-delivery

## Setting Up the Project with Rye

https://rye.astral.sh/

1. **Install Rye**:
   ```sh
   curl -sSf https://rye.astral.sh/get | bash
   ```
   
2. **Source env variables**:
   ```sh
   source "$HOME/.rye/env"
   ```
   
3. **Set up the project**:
   ```sh
   rye sync
   ```   

4. **Run tests**:
   ```sh
   rye test
   ```
   

## Setting Up the Project with Make

1. **Install**:
   ```sh
   make install
   ```
   
2. **Run tests**:
   ```sh
   make test
   ```
   
## Setting Up the Project with Brew

1. **Install Rye (if not installed)**:
   ```sh
   brew install rye
   ```
   
2. **Set up the project**:
   ```sh
   rye sync
   ```   

3. **Run tests**:
   ```sh
   rye test
   ```