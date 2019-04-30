//
// Created by duncan on 4/30/19.
//


#ifndef CORRESPONSEGROUPING_CORRESPGROUP_H
#define CORRESPONSEGROUPING_CORRESPGROUP_H

#include <pcl/point_cloud.h>

namespace N {
    class CorrespGroup {
    public:
        void find (std::string model_filename_, std::string scene_filename_);
    };
}


#endif //CORRESPONSEGROUPING_CORRESPGROUP_H
