start=$SECONDS

sh edge-generator.sh
sh case-generator.sh
sh peaks-generator.sh
sh vaccinated-count-generator.sh
sh vaccination-population-ratio-generator.sh
sh vaccine-type-ratio-generator.sh
sh vaccinated-ratio-generator.sh
sh complete-vaccination-generator.sh

end=$SECONDS

echo "duration: $((end-start)) seconds."