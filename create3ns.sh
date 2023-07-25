#!/bin/bash
#A bash script to create 3 simple network namespaces
for i in 1 2 3
do
  ip netns add h$i
  ip link add vnet$i type veth peer name eth0 address 00:00:00:00:00:$i$i
  ip link set eth0 netns h$i up
  ip netns exec h$i ip addr add 10.0.0.$i/24 dev eth0
  ip netns exec h$i ip link set eth0 up
  ip netns exec h$i ip link set lo up
  ip link set vnet$i up
done
