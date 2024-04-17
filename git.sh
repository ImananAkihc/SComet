#!/bin/bash
AUTHOR=$1
PROJECT=$2
 
while(true);
do
{
  echo "doing clone ..."
  git clone  https://github.com/$AUTHOR/$PROJECT
  if [ $? -eq 0 ];then
    echo "clone success"
    break
  else
    echo "clone failed"
  fi
  rm -rf $PROJECT
  sleep 1;
} 
done
cd  $PROJECT
while(true);
do
{
  echo "doing submodule init ..."
  git submodule init 
  if [ $? -eq 0 ];then
    echo "init success "
    break
  else
    echo "init failed"
  fi
  #rm -rf $PROJECT
  sleep 1;
} 
done
 
while(true);
do
{
  echo "doing submodule update ..."
  git submodule update 
  if [ $? -eq 0 ];then
    echo "update success"
    break
  else
    echo "update failed"
  fi
  #rm -rf $PROJECT
  sleep 1;
} 
done
 