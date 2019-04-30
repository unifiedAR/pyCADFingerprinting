//
// Created by duncan on 4/23/19.
//

#ifndef CORRESPONDENCE_GROUPING_CORRESPGROUP_H
#define CORRESPONDENCE_GROUPING_CORRESPGROUP_H

#include <pcl/io/pcd_io.h>
#include <pcl/point_cloud.h>
#include <pcl/correspondence.h>
#include <pcl/features/normal_3d_omp.h>
#include <pcl/features/shot_omp.h>
#include <pcl/features/board.h>
#include <pcl/filters/uniform_sampling.h>
#include <pcl/recognition/cg/hough_3d.h>
#include <pcl/recognition/cg/geometric_consistency.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/kdtree/kdtree_flann.h>
#include <pcl/kdtree/impl/kdtree_flann.hpp>
#include <pcl/common/transforms.h>
#include <pcl/console/parse.h>
#include <iostream>


class CorrespGroup {
private:
    CorrespGroup() {int argc, char *argv[]}

    std::string model_filename_;
    std::string scene_filename_;

    typedef pcl::PointXYZRGBA PointType;
    typedef pcl::Normal NormalType;
    typedef pcl::ReferenceFrame RFType;
    typedef pcl::SHOT352 DescriptorType;;

    //Algorithm params
    bool show_keypoints_ (false);
    bool show_correspondences_ (false);
    bool use_cloud_resolution_ (false);
    bool use_hough_ (true);
    float model_ss_ (0.01f);
    float scene_ss_ (0.03f);
    float rf_rad_ (0.015f);
    float descr_rad_ (0.02f);
    float cg_size_ (0.01f);
    float cg_thresh_ (5.0f);

    void parseArguments(argc, argv, ".pcd")

    struct mainFunction();
};


#endif //CORRESPONDENCE_GROUPING_CORRESPGROUP_H