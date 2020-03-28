// version: 1.0.0
import jetbrains.buildServer.configs.kotlin.v2018_2.*
import buildTypes.*
import config.*
import scripts.addEnvParams
import scripts.addVcsRoot

// Version of TeamCity in which kotlin code was generated.
// It is used to convert settings from older TeamCity versions.
// If not specified, generated settings are treated as up-to-date.
version = "2019.1"

fun setBuildParameter() {
    /* toolchain params */
    repoName = "dany_meta_library_template"
    dockerContainerTimeoutInSeconds = 7200
    /* gitlab params */
    vcsGroup = "daniel"
    /* docker container params */
    useWindowsContainer = false
    dockerImageVersion = "1.0.0"
    dockerImageName = "dany_python36.centos"
}

project {
    setBuildParameter()

    // order of the buildtypes (default: alphabetically)
    buildTypesOrder = listOf(
            PullDockerImage,
            SetEnvParams,
            StartDockerContainer,
            GitCheckoutInDocker,
            InstallToolchainHelperScripts,
            InstallPythonRequirements,
            Pep8Check,
            PylintCheck,
            CheckTestCoverage,
            CustomCheck,
            BuildAndCommitRstDocFiles,
            CheckUpsourceReview,
            PublishPythonPackage,
            BuildAndPublishDocumentation,
            CreateMergeRequest,
            ShutdownDockerContainer,
            RunBuild
    )

    sequence {
        build(PullDockerImage)
        build(addVcsRoot(SetEnvParams, DslContext.settingsRoot)) {
            dependsOn(PullDockerImage, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(StartDockerContainer)) {
            dependsOn(SetEnvParams, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(GitCheckoutInDocker)) {
            dependsOn(StartDockerContainer, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(InstallToolchainHelperScripts)) {
            dependsOn(GitCheckoutInDocker, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(InstallPythonRequirements)) {
            dependsOn(InstallToolchainHelperScripts, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(Pep8Check)) {
            dependsOn(InstallToolchainHelperScripts, settingsCancelOnCancelAndCancelOnFailure)
        }
        build(addEnvParams(PylintCheck)) {
            dependsOn(Pep8Check, settingsCancelOnCancelAndIgnoreOnFailure)
        }
        build(addEnvParams(CheckTestCoverage)) {
            dependsOn(PylintCheck, settingsCancelOnCancelAndIgnoreOnFailure)
        }
        build(addEnvParams(CustomCheck)) {
            dependsOn(CheckTestCoverage, settingsCancelOnCancelAndIgnoreOnFailure)
        }
        build(addEnvParams(BuildAndCommitRstDocFiles)) {
            dependsOn(CustomCheck, settingsCancelOnCancelAndIgnoreOnFailure)
        }
        build(addEnvParams(CheckUpsourceReview)) {
            dependsOn(BuildAndCommitRstDocFiles, settingsCancelOnCancelAndIgnoreOnFailure)
        }
        build(addEnvParams(PublishPythonPackage)) {
            dependsOn(Pep8Check, settingsCancelOnCancelAndFailToStartOnFailure)
            dependsOn(PylintCheck, settingsCancelOnCancelAndFailToStartOnFailure)
            dependsOn(CheckTestCoverage, settingsCancelOnCancelAndFailToStartOnFailure)
            dependsOn(CustomCheck, settingsCancelOnCancelAndFailToStartOnFailure)
            dependsOn(BuildAndCommitRstDocFiles, settingsCancelOnCancelAndFailToStartOnFailure)
            dependsOn(CheckUpsourceReview, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(BuildAndPublishDocumentation)) {
            dependsOn(PublishPythonPackage, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(CreateMergeRequest)) {
            dependsOn(BuildAndPublishDocumentation, settingsCancelOnCancelAndFailToStartOnFailure)
        }
        build(addEnvParams(ShutdownDockerContainer)) {
            dependsOn(CreateMergeRequest, settingsIgnoreOnCancelAndIgnoreOnFailure)
        }
        build(RunBuild) {
            dependsOn(CreateMergeRequest, settingsCancelOnCancelAndFailToStartOnFailure)
            dependsOn(ShutdownDockerContainer, settingsIgnoreOnCancelAndIgnoreOnFailure)
        }
    }
}
