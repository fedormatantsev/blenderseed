
#
# This source file is part of appleseed.
# Visit http://appleseedhq.net/ for additional information and resources.
#
# This software is released under the MIT license.
#
# Copyright (c) 2014-2017 The appleseedhq Organization
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import multiprocessing

import bpy

try:
    threads = multiprocessing.cpu_count()
    max_threads = threads
except:
    threads = 1
    max_threads = 32


def scene_enumerator(self, context):
    matches = []
    for scene in bpy.data.scenes:
        matches.append((scene.name, scene.name, ""))
    return matches


def camera_enumerator(self, context):
    return object_enumerator('CAMERA')


class AppleseedRenderSettings(bpy.types.PropertyGroup):

    def update_stamp(self, context):
        self.render_stamp += self.render_stamp_patterns

    # Scene render settings.

    threads_auto = bpy.props.BoolProperty(name="threads_auto",
                                          description="Automatically determine the number of rendering threads",
                                          default=True)

    threads = bpy.props.IntProperty(name="threads",
                                    description="Number of threads to use for rendering",
                                    default=threads,
                                    min=1,
                                    max=max_threads)

    generate_mesh_files = bpy.props.BoolProperty(name="Export Geometry",
                                                 description="Write geometry to disk as .obj files",
                                                 default=True)

    export_mode = bpy.props.EnumProperty(name="Export Mode",
                                         description="Geometry export mode",
                                         items=[('all', "All", "Export all geometry, overwriting existing .obj files"),
                                                ('partial', "Partial", "Only export geometry that has not been written to disk"),
                                                ('selected', "Selected", "Only export selected geometry")],
                                         default='all')

    clean_cache = bpy.props.BoolProperty(name="clean_cache",
                                         description="Delete external files after rendering completes",
                                         default=False)

    export_hair = bpy.props.BoolProperty(name="export_hair",
                                         description="Export hair particle systems as renderable geometry",
                                         default=False)

    # Sampling.

    decorrelate_pixels = bpy.props.BoolProperty(name="decorrelate_pixels",
                                                description='Avoid correlation patterns at the expense of slightly more sampling noise',
                                                default=True)

    tile_width = bpy.props.IntProperty(name="tile_width",
                                       description="Set the width of the render tile",
                                       default=64,
                                       min=1)

    tile_height = bpy.props.IntProperty(name="tile_height",
                                        description="Set the height of the render tile",
                                        default=64,
                                        min=1)

    pixel_filter = bpy.props.EnumProperty(name="Pixel Filter",
                                          description="Pixel filter to use",
                                          items=[("blackman-harris", "Blackman-Harris", "Blackman-Harris"),
                                                 ("box", "Box", "Box"),
                                                 ("catmull", "Catmull-Rom Spline", "Catmull-Rom Spline"),
                                                 ("bspline", "Cubic B-spline", "Cubic B-spline"),
                                                 ("gaussian", "Gaussian", "Gaussian"),
                                                 ("lanczos", "Lanczos", "Lanczos"),
                                                 ("mitchell", "Mitchell-Netravali", "Mitchell-Netravali"),
                                                 ("triangle", "Triangle", "Triangle")],
                                          default="blackman-harris")

    pixel_filter_size = bpy.props.FloatProperty(name="pixel_filter_size",
                                                description="Pixel filter size",
                                                min=0.5,
                                                max=16.0,
                                                default=1.5)

    enable_render_stamp = bpy.props.BoolProperty(name="enable_render_stamp",
                                                 description="Enable a stamp on the output image",
                                                 default=False)

    render_stamp = bpy.props.StringProperty(name="render_stamp",
                                            description="Render stamp text",
                                            default="appleseed {lib-version} | Time: {render-time}")

    render_stamp_patterns = bpy.props.EnumProperty(name="Stamp Variables",
                                                   description="Variables to insert into the render stamp",
                                                   items=[
                                                       ('{lib-version}', "Library Version", ""),
                                                       ('{lib-name}', "Library Name", ""),
                                                       ('{lib-variant}', "Library Variant", ""),
                                                       ('{lib-config}', "Library Configuration", ""),
                                                       ('{lib-build-date}', "Library Build Date", ""),
                                                       ('{lib-build-time}', "Library Build Time", ""),
                                                       ('{render-time}', "Render Time", ""),
                                                       ('{peak-memory}', "Peak Memory", "")],
                                                   default='{render-time}',
                                                   update=update_stamp)

    pixel_sampler = bpy.props.EnumProperty(name="Pixel Sampler",
                                           description="Sampler",
                                           items=[("uniform", "Uniform", "Uniform"),
                                                  ("adaptive", "Adaptive", "Adaptive")],
                                           default="uniform")

    sampler_min_samples = bpy.props.IntProperty(name="sampler_min_samples",
                                                description="Minimum number of anti-aliasing samples",
                                                min=1,
                                                max=1000000,
                                                default=16,
                                                subtype='UNSIGNED')

    sampler_max_samples = bpy.props.IntProperty(name="sampler_max_samples",
                                                description="Maximum number of anti-aliasing samples",
                                                min=1,
                                                max=1000000,
                                                default=64,
                                                subtype='UNSIGNED')

    adaptive_sampler_enable_diagnostics = bpy.props.BoolProperty(name="adaptive_sampler_enable_diagnostics",
                                                                 description='',
                                                                 default=False)

    adaptive_sampler_quality = bpy.props.FloatProperty(name="adaptive_sampler_quality",
                                                       description='',
                                                       default=3.0,
                                                       min=0.0,
                                                       max=20.0,
                                                       precision=3)

    force_aa = bpy.props.BoolProperty(name="force_aa",
                                      description="When using 1 sample/pixel and Force Anti-Aliasing is disabled, samples are placed at the center of pixels",
                                      default=True)

    renderer_passes = bpy.props.IntProperty(name="renderer_passes",
                                            description="Number of antialiasing passes",
                                            default=1,
                                            min=1,
                                            max=1000000)

    light_sampler = bpy.props.EnumProperty(name="Light Sampler",
                                           description="The method used for sampling lights",
                                           items=[('cdf', 'CDF', 'CDF'),
                                                  ('lighttree', 'Light Tree', 'Light Tree')],
                                           default='cdf')

    tile_ordering = bpy.props.EnumProperty(name="Tile Ordering",
                                           description="Tile ordering",
                                           items=[('linear', "Linear", "Linear"),
                                                  ('spiral', "Spiral", "Spiral"),
                                                  ('hilbert', "Hilbert", "Hilbert"),
                                                  ('random', "Random", "Random")],
                                           default='spiral')

    # Lighting engine.
    lighting_engine = bpy.props.EnumProperty(name="Lighting Engine",
                                             description="Light transport algorithm",
                                             items=[('pt', "Path Tracer", "Unidirectional Path Tracer"),
                                                    ('sppm', "SPPM", "Stochastic Progressive Photon Mapping")],
                                             default='pt')

    record_light_paths = bpy.props.BoolProperty(name="record_light_paths",
                                                default=False)

    # DRT settings.

    enable_ibl = bpy.props.BoolProperty(name="enable_ibl",
                                        description="Enable Image-based lighting",
                                        default=True)

    enable_caustics = bpy.props.BoolProperty(name="enable_caustics",
                                             description="Enable caustics",
                                             default=False)

    enable_dl = bpy.props.BoolProperty(name="enable_dl",
                                       description="Enable direct lighting",
                                       default=True)

    next_event_estimation = bpy.props.BoolProperty(name="next_event_estimation",
                                                   description="Explicitly connect path vertices to light sources to improve efficiency",
                                                   default=True)

    max_bounces_unlimited = bpy.props.BoolProperty(name="max_bounces_unlimited",
                                                   description="No limit to number of ray bounces",
                                                   default=True)

    max_bounces = bpy.props.IntProperty(name="max_bounces",
                                        description="Maximum number of ray bounces",
                                        default=8,
                                        min=0)

    max_diffuse_bounces_unlimited = bpy.props.BoolProperty(name="max_diffuse_bounces_unlimited",
                                                           description="No limit to number of diffuse ray bounces",
                                                           default=True)

    max_diffuse_bounces = bpy.props.IntProperty(name="max_diffuse_bounces",
                                                description="Maximum total number of diffuse bounces",
                                                default=8,
                                                min=0)

    max_glossy_brdf_bounces_unlimited = bpy.props.BoolProperty(name="max_glossy_brdf_bounces_unlimited",
                                                               description="No limit to number of glossy ray bounces",
                                                               default=True)

    max_glossy_brdf_bounces = bpy.props.IntProperty(name="max_glossy_brdf_bounces",
                                                    description="Maximum total number of glossy bounces",
                                                    default=8,
                                                    min=0)

    max_specular_bounces_unlimited = bpy.props.BoolProperty(name="max_specular_bounces_unlimited",
                                                            description="No limit to number of specular ray bounces",
                                                            default=True)

    max_specular_bounces = bpy.props.IntProperty(name="max_specular_bounces",
                                                 description="Maximum total number of specular bounces",
                                                 default=8,
                                                 min=0)

    max_volume_bounces_unlimited = bpy.props.BoolProperty(name="max_volume_bounces_unlimited",
                                                          description="No limit to number of volume ray bounces",
                                                          default=True)

    max_volume_bounces = bpy.props.IntProperty(name="max_volume_bounces",
                                               description="Maximum total number of volume bounces",
                                               default=8,
                                               min=-0)

    max_ray_intensity_unlimited = bpy.props.BoolProperty(name="max_ray_intensity_unlimited",
                                                         description="Unlimited ray intensity",
                                                         default=True)

    max_ray_intensity = bpy.props.FloatProperty(name="max_ray_intensity",
                                                description="Clamp intensity of rays (after the first bounce) to this value to reduce fireflies",
                                                default=1.0,
                                                min=0)

    rr_start = bpy.props.IntProperty(name="rr_start",
                                     description="Consider pruning low contribution paths starting with this bounce",
                                     default=6,
                                     min=1,
                                     max=100)

    optimize_for_lights_outside_volumes = bpy.props.BoolProperty(name="optimize_for_lights_outside_volumes",
                                                                 description="Use when light sources are outside volumes",
                                                                 default=True)

    volume_distance_samples = bpy.props.IntProperty(name="volume_distance_samples",
                                                    description="Number of depth samples to take in a volume",
                                                    default=2,
                                                    min=0,
                                                    max=100)

    dl_light_samples = bpy.props.IntProperty(name="dl_light_samples",
                                             description="Number of samples used to estimate direct lighting",
                                             default=1,
                                             min=0,
                                             max=512)

    dl_low_light_threshold = bpy.props.FloatProperty(name="dl_low_light_threshold",
                                                     description="Light contribution threshold to disable shadow rays",
                                                     default=0.0,
                                                     min=0.0,
                                                     max=10.0)

    ibl_env_samples = bpy.props.IntProperty(name="ibl_env_samples",
                                            description="Number of samples used to estimate environment lighting",
                                            default=1,
                                            min=0,
                                            max=512)

    # SPPM settings.

    sppm_dl_mode = bpy.props.EnumProperty(name="Direct Lighting",
                                          description="SPPM Direct Lighting Component",
                                          items=[('rt', "RT Direct Lighting", 'Use ray tracing to estimate direct lighting'),
                                                 ('sppm', "SPPM Direct Lighting", 'Use photon maps to estimate direct lighting'),
                                                 ('off', "No Direct Lighting", 'Do not estimate direct lighting')],
                                          default='rt')

    # SPPM photon tracing settings.

    sppm_photon_max_length = bpy.props.IntProperty(name="sppm_photon_max_length",
                                                   description="Maximum path length for photons (0 = unlimited)",
                                                   default=0,
                                                   min=0,
                                                   max=100)

    sppm_photon_rr_start = bpy.props.IntProperty(name="sppm_photon_rr_start",
                                                 description="Consider pruning low contribution photons starting with this bounce",
                                                 default=6,
                                                 min=1,
                                                 max=100)

    sppm_env_photons = bpy.props.IntProperty(name="sppm_env_photons",
                                             description="Number of environment photons per render pass",
                                             default=1000000,
                                             min=0)

    sppm_light_photons = bpy.props.IntProperty(name="sppm_light_photons",
                                               description="Number of light photons per render pass",
                                               default=1000000,
                                               min=0)

    # SPPM radiance estimation settings.

    sppm_pt_max_length = bpy.props.IntProperty(name="sppm_pt_max_length",
                                               description="Maximum number of path bounces (0 = unlimited)",
                                               default=0,
                                               min=0,
                                               max=100)

    sppm_pt_rr_start = bpy.props.IntProperty(name="sppm_pt_rr_start",
                                             description="Consider pruning low contribution paths starting with this bounce",
                                             default=6,
                                             min=1,
                                             max=100)

    sppm_initial_radius = bpy.props.FloatProperty(name="sppm_initial_radius",
                                                  description="Initial photon gathering radius in percent of the scene diameter",
                                                  default=0.1,
                                                  min=0.0,
                                                  max=100,
                                                  precision=3)

    sppm_max_per_estimate = bpy.props.IntProperty(name="sppm_max_per_estimate",
                                                  description="Maximum number of photons used to estimate radiance",
                                                  default=100,
                                                  min=1)

    sppm_alpha = bpy.props.FloatProperty(name="sppm_alpha",
                                         description="Evolution rate of photon gathering radius",
                                         default=0.7,
                                         min=0.0,
                                         max=1.0)

    # Miscellaneous settings.

    light_mats_radiance_multiplier = bpy.props.FloatProperty(name="light_mats_radiance_multiplier",
                                                             description="Multiply the exitance of light-emitting materials by this factor",
                                                             min=0.0,
                                                             max=100.0,
                                                             default=1.0)

    export_emitting_obj_as_lights = bpy.props.BoolProperty(name="export_emitting_obj_as_lights",
                                                           description="Export objects with light-emitting materials as mesh (area) lights",
                                                           default=True)

    # Denoiser settings

    enable_denoiser = bpy.props.BoolProperty(name="enable_denoiser",
                                             description="Use a post process denoising step on the finished image",
                                             default=False)

    prefilter_spikes = bpy.props.BoolProperty(name="prefilter_spikes",
                                              default=True)

    spike_threshold = bpy.props.FloatProperty(name="spike_threshold",
                                              default=2.0,
                                              min=0.1,
                                              max=4.0)

    patch_distance_threshold = bpy.props.FloatProperty(name="patch_distance_threshold",
                                                       default=1.0,
                                                       min=0.5,
                                                       max=3.0)

    denoise_scales = bpy.props.IntProperty(name="denoise_scales",
                                           default=3,
                                           min=1,
                                           max=10)

    # Motion blur settings.

    enable_motion_blur = bpy.props.BoolProperty(name="enable_motion_blur",
                                                description="Enable rendering of motion blur",
                                                default=False)

    enable_deformation_blur = bpy.props.BoolProperty(name="enable_deformation_blur",
                                                     description="Global toggle for rendering of deformation motion blur. Warning: objects with deformation motion blur enabled will add to export time.",
                                                     default=False)

    enable_object_blur = bpy.props.BoolProperty(name="enable_object_blur",
                                                description="Global toggle for rendering of object motion blur",
                                                default=False)

    enable_camera_blur = bpy.props.BoolProperty(name="enable_camera_blur",
                                                description="Enable rendering of camera motion blur",
                                                default=False)

    shutter_open = bpy.props.FloatProperty(name="shutter_open",
                                           description="Shutter open time (relative to start of current frame)",
                                           default=0.0,
                                           min=0.0,
                                           max=0.999,
                                           step=3,
                                           precision=3)

    shutter_close = bpy.props.FloatProperty(name="shutter_close",
                                            description="Shutter close time (relative to end of current frame)",
                                            default=1.0,
                                            min=0.001,
                                            max=1.0,
                                            step=3,
                                            precision=3)


def register():
    bpy.utils.register_class(AppleseedRenderSettings)
    bpy.types.Scene.appleseed = bpy.props.PointerProperty(type=AppleseedRenderSettings)


def unregister():
    del bpy.types.Scene.appleseed
    bpy.utils.unregister_class(AppleseedRenderSettings)
