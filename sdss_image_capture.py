import os
import ssl
import urllib.request
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u

"""
    Get the right ascenscion (RA) and declination (DEC) degree values from the .csv file. We also drop
    the values for which the debiased values of either the elliptical galaxy probability or spiral 
    galaxy probability is less than 0.8.

    @param df: dataframe containing the degree coordinates
    @return dataframe containing the object ID, ra, and dec values from the .csv file with debiased
            values greater than 0.8 (we also keep the debiased probability columns)
"""
def drop_items(df):
    # Drop the values for which the debiased threshold is less than 0.8
    df = df[(df['P_EL_DEBIASED'] >= 0.8) | (df['P_CS_DEBIASED'] >= 0.8)]
    # Drop instances where 'UNCERTAIN' == 1 (only want elliptical and spiral from this dataset)
    df = df[(df['UNCERTAIN'] == 0)]
    
    # Now drop unecessary columns for gathering data
    df = df.drop(columns = ['NVOTE', 'P_EL', 'P_CW', 'P_ACW', 'P_EDGE', 'P_DK', 'P_MG', 
                            'P_CS', 'P_EL_DEBIASED', 'P_CS_DEBIASED', 'UNCERTAIN'])
    
    # Results in dataframe of [NUMBER_GALAXIES rows x 5(ID, ra, dec, spiral, elliptical) columns]
    return df.reset_index(drop = True)
    
"""
    Convert the original right ascenscion (RA) and declination (DEC) values from the .csv file
    which are in degrees to decimal units.

    @param ra: right ascenscion (RA) degree
    @param dec: declination (DEC) degree
    @return celestial coordinate in decimal units
"""
def convert_to_dec(ra, dec):
    dec_coord = SkyCoord(ra = ra, dec = dec, unit = (u.hourangle, u.deg))
    coordinates = dec_coord.to_string('decimal').split(' ')
    ra = coordinates[0]
    dec = coordinates[1]
    return ra, dec

"""
    Create new dataframe of object ID with converted celestial coordinates.

    @param df_orig: original dataframe with un-converted celestial coordinates
    @param new dataframe containing object ID with converted celestial coordinates
"""
def convert_df(df_orig):
    ra_list = df_orig['RA'].tolist()
    dec_list = df_orig['DEC'].tolist()

    converted_ra = []
    converted_dec = []

    for ra, dec in zip(ra_list, dec_list):
        new_ra, new_dec = convert_to_dec(ra, dec) # SkyCoord object
        converted_ra.append(new_ra) # Appends a string
        converted_dec.append(new_dec) # Appends a string
    
    converted_ra_df = pd.DataFrame({'RA_DECIMAL':converted_ra})
    converted_dec_df = pd.DataFrame({'DEC_DECIMAL':converted_dec})
    frames = [df_orig['OBJID'], converted_ra_df, converted_dec_df, df_orig["SPIRAL"], df_orig["ELLIPTICAL"]]
    new_df = pd.concat(frames, axis = 1)
    return new_df
    
"""
    Get images based on the converted coordinates. Ensure the appropriate folder structure is in place. Will save 
    image as '.jpg' file.

    @param df_converted: dataframe containing object ID, converted right ascenscion (RA) decimal coordinate,
                        and declination (DEC) decimal coordinate
    @param NUMBER_ELLIPTICAL: number of elliptical galaxy images we would like to download
    @param NUMBER_SPIRAL: number of spiral galaxy images we would like to download
"""
def get_images(df_converted, NUMBER_ELLIPTICAL = 1000, NUMBER_SPIRAL = 1000):
    number_elliptical = 0
    number_spiral = 0

    spiral_done = False
    elliptical_done = False

    objid_list = df_converted['OBJID'].tolist()
    ra_list = df_converted['RA_DECIMAL'].tolist()
    dec_list = df_converted['DEC_DECIMAL'].tolist()

    # elliptical_list  = df_converted["ELLIPTICAL"].tolist()
    spiral_list  = df_converted["SPIRAL"].tolist()
    
    for objid, ra, dec, spiral in zip(objid_list, ra_list, dec_list, spiral_list):
        # Save the image using the 'OBJID' as .jpg image
        if spiral_done and elliptical_done:
          break
        
        filename = str(objid) + '.jpg'
        
        if spiral:
          if spiral_done or number_spiral > NUMBER_SPIRAL:
            spiral_done = True
            continue

          filename = os.path.join(OUTPUT_DIR, "spiral", filename)
          number_spiral+=1

        else:
          if elliptical_done or number_elliptical > NUMBER_ELLIPTICAL:
            elliptical_done = True
            continue

          filename = os.path.join(OUTPUT_DIR, "elliptical", filename)
          number_elliptical +=1

        # Replace the ra and dec coordinates in the URL, downloading in 512 x 512 resolution
        try:
            image_url = "http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx?ra=" + str(ra) + "&dec=" + str(dec) + "&scale=0.15&width=512&height=512&opt="
            urllib.request.urlretrieve(image_url, filename) 
            # print("ObjID:", objid, "saved at:", filename)
        except:
            print("Image with object ID " + str(objid) + " and coordinates " + str(ra) + ", " + str(dec) + " not found.")
            continue # Continue to next set of coordinates and image retrieval
    
