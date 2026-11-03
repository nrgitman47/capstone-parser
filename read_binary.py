import struct
import numpy as np

# Open .svlog for reading
with open("2026-10-28-15-53.svlog", "rb") as file:

    # Create csv to write IMU data
    with open('IMU_data_s1.csv', 'w') as f_imu:
        f_imu.write("utc_msec, powerup_msec, vecx, vecy, vecz\n")

        # Create ATOF csv
        with open('ATOF_data_s1.csv', 'w') as f_atof:
            f_atof.write("powerup_msec, utc_msec, Target_Index, Angle_Rad, TOF_Sec\n")

            while True:
                signature = file.read(2)
                if len(signature) == 0:
                    print("Done!")
                    break

                # First two bytes should be "B" and "R"
                #br = file.read(2)
                # The next two return packet length
                packet_length = int.from_bytes(file.read(2), 'little')
                print(packet_length, "bytes")
                # The packet ID (defines parameter type, IMU vs ATOF etc)
                packet_id = int.from_bytes(file.read(2), 'little')
                # Source Device ID (u8)
                src_device_id = file.read(1)
                # Destination Device ID (u8)
                dst_device_id = file.read(1)
                # Payload
                payload = file.read(packet_length)
                # Checksum
                checksum = int.from_bytes(file.read(2), 'little')

                if packet_id == 504:
                    print("IMU data")
                    # pull IMU vectors
                    vecx, vecy, vecz, d1, d2, d3, utc_msec, pwr_up_msec = struct.unpack('<ffffffQI', payload)

                    # calculate roll angle (rad)
                    roll_i = np.atan2(vecy,vecz)
                    # calculate pitch angle (rad)
                    pitch_i = np.asin(vecx)

                    # write to csv
                    f_imu.write(f"{utc_msec}, {pwr_up_msec}, {vecx}, {vecy}, {vecz}\n")
                if packet_id == 3012:
                    print("ATOF data")
                    prec_bytes = 40 # number of bytes preceding the actual atof data
                    pwr_up_msec, utc_msec, listening_sec, sos_mps, ping_number, ping_hz, pulse_sec, d1, num_points, d2 = struct.unpack('<IQffIIfIHH', payload[0:prec_bytes])
                    atof = payload[prec_bytes:packet_length]

                    target_index = 0
                    for angle, tof, res1, res2 in struct.iter_unpack('<ffII', atof):
                        text = f"{pwr_up_msec},{utc_msec},{target_index},{angle},{tof}\n"
                        f_atof.write(text)
                        target_index = target_index + 1

