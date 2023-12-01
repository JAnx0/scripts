#!/usr/bin/env bash

error_and_exit() {
	echo "[-] Unable to mount shared folders. Make sure vmware-tools are installed correctly" 
	exit
}


# create mount directory
sudo mkdir /mnt/hgfs

# create rc.local file (often missing)
if $(sudo touch /etc/rc.local);
then
	# mount shared folders into mount directory 
	if $(sudo mount -t fuse.vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other);
	then
		# change file ownership
		if $(sudo chown root /etc/rc.local); 
		then
			# adjust file permissions
			if $(sudo chmod 755 /etc/rc.local);
			then
				echo "[+] Successfully mounted VMWare shared folder to /mnt/hgfs!"
			else
				error_and_exit
			fi
		else
			error_and_exit
		fi
	else
		error_and_exit
	fi
else
	error_and_exit
fi
