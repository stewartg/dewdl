nexus_host="nexus.corp.icr-team.com"
pypi_host="pypi.python.org"
nexus_pyindex="https://$nexus_host/repository/erudition-pypi/simple"
base_pyindex="https://$pypi_host/simple"
echo "[global]" > $1/pip.conf
echo "index = $nexus_pyindex" >> $1/pip.conf
echo "index-url = $nexus_pyindex" >> $1/pip.conf
echo "extra-index-url = $base_pyindex" >> $1/pip.conf
echo "trusted-host = $nexus_host $pypi_host" >> $1/pip.conf
