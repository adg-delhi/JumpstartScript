#!/bin/bash
if [ ! -f /usr/local/bin/JumpstartScript ]
    then
        cp JumpstartScript.sh "/usr/local/bin/JumpstartScript"
    else
        echo "JumpstartScript already exist in your /usr/local/bin folder. To update first delete it from the folder and run the script again."
    fi


if [ -z $1 ]
    then
        echo "Please Use ./JumpstartScript.sh <DirectoryName>. We will create this directory under ."+ $PWD+"/"+"<DirectoryName>"
        exit 1
    fi


mkdir $1
cd $1

mkdir temp
cd temp

# Cloning the generator
echo "Copying requisite dependencies in " + $PWD
git clone https://github.com/moldedbits/generator-jumpstart-generator.git

if brew ls --versions == null
    then
        echo "HomeBrew is not installed. Please install HomeBrew and Try again........................"
    else 
        echo "HomeBrew is installed..................................................................."
        # Installing the Node Package
        if which node == null
            then 
                echo "Node is not installed..........................................................."
                echo "Installing Node................................................................."
                brew install node
            else
                echo "Node is installed."
            fi

        if which npm  == null
            then
                # Installing NPM
                echo "Installing NPM............................................................................"
                npm install npm@latest -g
            else
                # Updating Npm
                echo "Updating NPM............................................................................"
                npm update -g
            fi

        if which yo == null
            then
                # Installing Yo
                echo "Installing Yeoman............................................................................."
                npm install --global yo
            else
                echo "Yeoman Already Installed..................................................................."
            fi

        OUTPUT="$(yo --generators | grep generator)"

        if ${OUTPUT} == null
            then
                # Installing Yeoman's generator.generator
                echo "Installing Required Generators............................................................................"
                npm install -g generator-generator
            else
                 echo "Already Have Required Generators............................................................................"
            fi

        cd generator-jumpstart-generator
        
        # Linking with npm
        echo "Linking NPM............................................................................"
        npm link
        
        cd ../..

        yo jumpstart-generator
    fi

echo "Removing dependencies........................................................................."
rm -rf temp

#echo $PWD 
#cd ..
#echo $PWD 
#echo 'export APP='$PWD >> ~/.bashrc 